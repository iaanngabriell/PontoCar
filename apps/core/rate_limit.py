from dataclasses import dataclass
from hashlib import sha256
from math import ceil

from django.db import IntegrityError, transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone


from .models import RateLimitBucket


@dataclass(frozen=True)
class RateLimitResult:
    permitido: bool
    retry_after: int = 0


def _hash_chave(chave):
    return sha256(chave.encode("utf-8")).hexdigest()


def obter_ip_cliente(request):
    """
    Obtém o IP original em ambientes atrás de proxy/reverse proxy, como Vercel.

    O primeiro endereço de X-Forwarded-For representa o cliente original.
    Em desenvolvimento local, cai para REMOTE_ADDR.
    """
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR") or "desconhecido"


def consumir_limite(*, chave, limite, janela_segundos):
    """
    Consome uma tentativa de uma janela fixa persistida no PostgreSQL.
    """
    if limite < 1:
        raise ValueError("limite deve ser maior que zero.")

    if janela_segundos < 1:
        raise ValueError("janela_segundos deve ser maior que zero.")

    chave_hash = _hash_chave(chave)
    agora = timezone.now()

    with transaction.atomic():
        bucket = (
            RateLimitBucket.objects.select_for_update()
            .filter(chave=chave_hash)
            .first()
        )

        if bucket is None:
            try:
                with transaction.atomic():
                    RateLimitBucket.objects.create(
                        chave=chave_hash,
                        contador=1,
                        inicio_janela=agora,
                    )
                return RateLimitResult(permitido=True)
            except IntegrityError:
                bucket = RateLimitBucket.objects.select_for_update().get(
                    chave=chave_hash
                )

        decorrido = max(
            0,
            (agora - bucket.inicio_janela).total_seconds(),
        )

        if decorrido >= janela_segundos:
            bucket.contador = 1
            bucket.inicio_janela = agora
            bucket.save(
                update_fields=[
                    "contador",
                    "inicio_janela",
                    "atualizado_em",
                ]
            )
            return RateLimitResult(permitido=True)

        if bucket.contador >= limite:
            retry_after = max(
                1,
                ceil(janela_segundos - decorrido),
            )
            return RateLimitResult(
                permitido=False,
                retry_after=retry_after,
            )

        bucket.contador += 1
        bucket.save(
            update_fields=[
                "contador",
                "atualizado_em",
            ]
        )

    return RateLimitResult(permitido=True)


def limpar_limite(chave):
    """
    Limpa um contador específico.
    """
    RateLimitBucket.objects.filter(
        chave=_hash_chave(chave)
    ).delete()


def _formatar_retry_after(segundos):
    if segundos < 60:
        return f"{segundos} segundo(s)"

    minutos = ceil(segundos / 60)
    if minutos < 60:
        return f"{minutos} minuto(s)"

    horas = ceil(minutos / 60)
    return f"{horas} hora(s)"


def _request_espera_json(request):
    accept = request.headers.get("Accept", "")
    requested_with = request.headers.get("X-Requested-With", "")
    return "application/json" in accept or requested_with == "XMLHttpRequest"


def resposta_limite_excedido(
    request,
    resultado,
    mensagem="Muitas tentativas. Aguarde alguns instantes e tente novamente.",
    titulo="Muitas tentativas detectadas",
    voltar_url=None,
):
    """
    Produz uma resposta HTTP 429 amigável para HTML e JSON para clientes
    que não esperam página.
    """
    retry_after = max(1, resultado.retry_after)
    headers = {
        "Retry-After": str(retry_after),
        "Cache-Control": "no-store",
    }

    if _request_espera_json(request):
        return JsonResponse(
            {
                "detail": mensagem,
                "retry_after": retry_after,
                "status_code": 429,
            },
            status=429,
            headers=headers,
        )

    response = render(
        request,
        "errors/429.html",
        {
            "titulo": titulo,
            "mensagem": mensagem,
            "retry_after": retry_after,
            "retry_after_humano": _formatar_retry_after(retry_after),
            "voltar_url": voltar_url,
        },
        status=429,
    )

    for chave, valor in headers.items():
        response[chave] = valor

    return response