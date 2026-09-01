from django.db.models import Q
from django.shortcuts import render

from .models import Servico


def lista(request):
    busca = request.GET.get("q", "").strip()
    servicos = Servico.objects.filter(empresa__ativa=True).select_related("empresa", "empresa__localizacao")
    if busca:
        servicos = servicos.filter(
            Q(nome__icontains=busca)
            | Q(descricao__icontains=busca)
            | Q(empresa__nome_fantasia__icontains=busca)
        )
    return render(request, "servicos/lista.html", {"servicos": servicos.order_by("nome"), "busca": busca})
