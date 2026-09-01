from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import render

from apps.usuarios.models import Usuario

from .models import Venda


def _eh_administrador(user):
    return user.is_authenticated and (
        user.is_staff
        or user.is_superuser
        or user.tipo_usuario == Usuario.TipoUsuario.ADMINISTRADOR
    )


@login_required
def comprador_compras(request):
    compras = (
        Venda.objects.filter(comprador=request.user, status=Venda.StatusVenda.CONCLUIDA)
        .select_related("veiculo", "veiculo__proprietario_atual")
        .order_by("-data_proposta")
    )
    return render(request, "vendas/comprador_compras.html", {"compras": compras})


@user_passes_test(_eh_administrador)
def admin_vendas(request):
    busca = request.GET.get("q", "").strip()
    vendas = Venda.objects.select_related("comprador", "veiculo", "veiculo__proprietario_atual").order_by("-data_proposta")
    if busca:
        vendas = vendas.filter(
            Q(veiculo__marca__icontains=busca)
            | Q(veiculo__modelo__icontains=busca)
            | Q(veiculo__placa__icontains=busca)
            | Q(comprador__email__icontains=busca)
        )
    return render(request, "vendas/admin_vendas.html", {"vendas": vendas, "busca": busca})
