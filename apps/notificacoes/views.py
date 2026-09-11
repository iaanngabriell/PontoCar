from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models import Notificacao


def _redirecionar_seguro(request, destino, fallback="notificacoes:lista"):
    """Aceita apenas destinos locais/permitidos e evita open redirect."""
    if destino and url_has_allowed_host_and_scheme(
        url=destino,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(destino)
    return redirect(fallback)


@login_required
def lista(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user)[:50]
    return render(
        request,
        "notificacoes/lista.html",
        {"notificacoes": notificacoes},
    )


@login_required
@require_POST
def abrir(request, notificacao_id):
    notificacao = get_object_or_404(
        Notificacao,
        id=notificacao_id,
        usuario=request.user,
    )
    if not notificacao.lida:
        notificacao.lida = True
        notificacao.lida_em = timezone.now()
        notificacao.save(update_fields=("lida", "lida_em"))

    return _redirecionar_seguro(request, notificacao.url)


@login_required
@require_POST
def marcar_todas_lidas(request):
    Notificacao.objects.filter(usuario=request.user, lida=False).update(
        lida=True,
        lida_em=timezone.now(),
    )
    return _redirecionar_seguro(request, request.POST.get("next", ""))
