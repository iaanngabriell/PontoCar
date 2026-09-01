from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.empresas.models import Empresa

from .models import ApoliceSeguro, Seguro


def lista(request):
    empresa_id = request.GET.get("empresa", "").strip()
    seguros = (
        Seguro.objects.filter(
            ativo=True,
            empresa__ativa=True,
            empresa__tipo_empresa__in=[
                Empresa.TipoEmpresa.SEGURADORA,
                Empresa.TipoEmpresa.CORRETORA,
            ],
        )
        .select_related("empresa")
        .order_by("valor_referencia", "nome")
    )
    if empresa_id:
        seguros = seguros.filter(empresa_id=empresa_id)

    empresas = (
        Empresa.objects.filter(
            ativa=True,
            tipo_empresa__in=[Empresa.TipoEmpresa.SEGURADORA, Empresa.TipoEmpresa.CORRETORA],
            seguros__ativo=True,
        )
        .distinct()
        .order_by("nome_fantasia")
    )
    return render(
        request,
        "seguros/lista.html",
        {"seguros": seguros, "empresas": empresas, "empresa_atual": empresa_id},
    )


@login_required
def comprador_cotacoes(request):
    status = request.GET.get("status", "").strip()
    apolices = (
        ApoliceSeguro.objects.filter(contratante=request.user)
        .select_related("seguro", "seguro__empresa", "veiculo")
        .order_by("-inicio_vigencia")
    )
    if status:
        apolices = apolices.filter(status=status)
    return render(
        request,
        "seguros/comprador_cotacoes.html",
        {
            "apolices": apolices,
            "status_atual": status,
            "status_choices": ApoliceSeguro.StatusApolice.choices,
        },
    )
