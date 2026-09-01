from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.empresas.models import Empresa
from apps.leads.models import Lead
from apps.veiculos.models import Veiculo

from .models import Favorito
from .services import alternar_favorito


def _foto_exibicao(veiculo):
    fotos = list(veiculo.fotos.all())
    return next((foto for foto in fotos if foto.principal), fotos[0] if fotos else None)


def _anunciante(veiculo):
    if not veiculo.proprietario_atual_id:
        return "Anunciante indisponível"
    empresa = (
        Empresa.objects.filter(representante=veiculo.proprietario_atual, ativa=True)
        .order_by("data_cadastro")
        .first()
    )
    if empresa:
        return empresa.nome_fantasia
    return veiculo.proprietario_atual.get_full_name() or veiculo.proprietario_atual.email


@login_required
def comprador_interesses(request):
    aba = request.GET.get("aba", "interesses")
    interesses = list(
        Lead.objects.filter(comprador=request.user)
        .select_related("veiculo", "veiculo__proprietario_atual")
        .prefetch_related("veiculo__fotos")
        .order_by("-data_criacao")
    )
    favoritos = list(
        Favorito.objects.filter(usuario=request.user)
        .select_related("veiculo", "veiculo__proprietario_atual")
        .prefetch_related("veiculo__fotos")
        .order_by("-data_criacao")
    )

    for lead in interesses:
        lead.veiculo.foto_exibicao = _foto_exibicao(lead.veiculo)
        lead.veiculo.anunciante_nome = _anunciante(lead.veiculo)
    for favorito in favoritos:
        favorito.veiculo.foto_exibicao = _foto_exibicao(favorito.veiculo)
        favorito.veiculo.anunciante_nome = _anunciante(favorito.veiculo)

    return render(
        request,
        "favoritos/comprador_interesses.html",
        {
            "aba": aba,
            "interesses": interesses,
            "favoritos": favoritos,
            "interesses_total": len(interesses),
            "favoritos_total": len(favoritos),
        },
    )


@login_required
@require_POST
def alternar(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    ativo = alternar_favorito(usuario=request.user, veiculo=veiculo)
    messages.success(request, "Veículo adicionado aos favoritos." if ativo else "Veículo removido dos favoritos.")

    proximo = request.POST.get("next", "")
    if proximo and url_has_allowed_host_and_scheme(
        url=proximo,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(proximo)
    return redirect(reverse("veiculos:detalhes", kwargs={"veiculo_id": veiculo.id}))
