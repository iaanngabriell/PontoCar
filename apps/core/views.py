from django.shortcuts import render

from apps.empresas.models import Empresa
from apps.veiculos.models import Veiculo


def index(request):
    veiculos_destaque = (
        Veiculo.objects.filter(status=Veiculo.StatusVeiculo.DISPONIVEL)
        .select_related("proprietario_atual")
        .prefetch_related("fotos")
        .order_by("-data_cadastro")[:6]
    )
    empresas_destaque = (
        Empresa.objects.filter(ativa=True)
        .select_related("localizacao")
        .order_by("-data_cadastro")[:5]
    )
    return render(
        request,
        "core/index.html",
        {
            "veiculos_destaque": veiculos_destaque,
            "empresas_destaque": empresas_destaque,
        },
    )


def sobre(request):
    return render(request, "core/sobre.html")
