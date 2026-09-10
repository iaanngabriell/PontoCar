from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Notificacao


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

    return redirect(notificacao.url or "notificacoes:lista")


@login_required
@require_POST
def marcar_todas_lidas(request):
    Notificacao.objects.filter(usuario=request.user, lida=False).update(
        lida=True,
        lida_em=timezone.now(),
    )
    return redirect(request.POST.get("next") or "notificacoes:lista")
