import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .foto_services import reordenar_fotos_veiculo
from .models import Veiculo


@login_required
@require_POST
def reordenar_fotos(request, veiculo_id):
    """Persiste a ordem das fotos de um anúncio pertencente ao usuário logado."""
    veiculo = get_object_or_404(
        Veiculo,
        id=veiculo_id,
        proprietario_atual=request.user,
    )

    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"ok": False, "erro": "Não foi possível interpretar a ordem enviada."},
            status=400,
        )

    foto_ids = payload.get("ordem")
    if not isinstance(foto_ids, list):
        return JsonResponse(
            {"ok": False, "erro": "Informe a ordem das fotos em uma lista."},
            status=400,
        )

    try:
        fotos = reordenar_fotos_veiculo(
            veiculo=veiculo,
            foto_ids=foto_ids,
        )
    except ValidationError as exc:
        mensagem = exc.messages[0] if exc.messages else "Ordem de fotos inválida."
        return JsonResponse({"ok": False, "erro": mensagem}, status=400)

    return JsonResponse(
        {
            "ok": True,
            "ordem": [str(foto.id) for foto in fotos],
            "principal": str(fotos[0].id) if fotos else None,
        }
    )
