from .models import Notificacao


def notificacoes_contexto(request):
    if not request.user.is_authenticated:
        return {
            "notificacoes_nao_lidas": 0,
            "notificacoes_recentes": (),
        }

    qs = Notificacao.objects.filter(usuario=request.user)
    return {
        "notificacoes_nao_lidas": qs.filter(lida=False).count(),
        "notificacoes_recentes": tuple(qs[:5]),
    }
