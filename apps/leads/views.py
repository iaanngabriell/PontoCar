from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Lead


@login_required
def vendedor_leads(request):
    status = request.GET.get("status", "").strip()
    leads = (
        Lead.objects.filter(veiculo__proprietario_atual=request.user)
        .select_related("veiculo", "comprador")
        .order_by("-data_criacao")
    )
    if status:
        leads = leads.filter(status=status)
    return render(
        request,
        "leads/vendedor_leads.html",
        {"leads": leads, "status_atual": status, "status_choices": Lead.Status.choices},
    )
