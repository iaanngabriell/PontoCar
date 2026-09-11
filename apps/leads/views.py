from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.core.rate_limit import (
    consumir_limite,
    resposta_limite_excedido,
)

from .forms import LeadMensagemForm, LeadRespostaForm
from .models import Lead
from .services import responder_como_interessado, responder_interesse


MENSAGEM_LIMITE_USUARIO = 12
MENSAGEM_JANELA_SEGUNDOS = 60


@login_required
def vendedor_leads(request):
    status = request.GET.get("status", "").strip()
    leads_qs = (
        Lead.objects.filter(
            Q(anunciante=request.user)
            | Q(anunciante__isnull=True, veiculo__proprietario_atual=request.user)
        )
        .select_related("veiculo", "comprador", "anunciante")
        .prefetch_related("mensagens", "mensagens__autor")
        .order_by("-data_criacao")
        .distinct()
    )
    if status:
        leads_qs = leads_qs.filter(status=status)

    leads = list(leads_qs)
    for lead in leads:
        lead.form_resposta = LeadRespostaForm(lead=lead, auto_id=False)

    return render(
        request,
        "leads/vendedor_leads.html",
        {
            "leads": leads,
            "status_atual": status,
            "status_choices": Lead.Status.choices,
        },
    )


@login_required
@require_POST
def responder_lead(request, lead_id):
    lead = get_object_or_404(
        Lead.objects.select_related("veiculo", "comprador", "anunciante"),
        Q(anunciante=request.user)
        | Q(anunciante__isnull=True, veiculo__proprietario_atual=request.user),
        id=lead_id,
    )

    resultado = consumir_limite(
        chave=f"mensagem:user:{request.user.pk}",
        limite=MENSAGEM_LIMITE_USUARIO,
        janela_segundos=MENSAGEM_JANELA_SEGUNDOS,
    )
    if not resultado.permitido:
        return resposta_limite_excedido(
            request,
            resultado,
            "Você enviou muitas mensagens em pouco tempo. Aguarde e tente novamente.",
            titulo="Envio de mensagens temporariamente bloqueado",
            voltar_url=reverse("leads:vendedor_leads"),
        )

    form = LeadRespostaForm(request.POST, lead=lead, auto_id=False)

    if not form.is_valid():
        erros = []
        for mensagens_erro in form.errors.values():
            erros.extend(str(item) for item in mensagens_erro)
        messages.error(request, " ".join(erros) or "Confira os dados da resposta.")
        return redirect(f"{reverse('leads:vendedor_leads')}#lead-{lead.id}")

    try:
        responder_interesse(
            lead=lead,
            anunciante=request.user,
            resposta=form.cleaned_data["resposta"],
            status=form.cleaned_data["status"],
        )
    except (ValidationError, PermissionDenied) as exc:
        texto = getattr(exc, "messages", None)
        messages.error(request, texto[0] if texto else str(exc))
    else:
        if lead.comprador_id:
            messages.success(request, "Mensagem enviada ao interessado.")
        else:
            messages.success(
                request,
                "Mensagem registrada. Como o interesse veio de um visitante, use também o e-mail ou telefone informado.",
            )

    return redirect(f"{reverse('leads:vendedor_leads')}#lead-{lead.id}")


@login_required
@require_POST
def responder_interessado(request, lead_id):
    lead = get_object_or_404(
        Lead.objects.select_related("veiculo", "comprador", "anunciante"),
        id=lead_id,
        comprador=request.user,
    )

    resultado = consumir_limite(
        chave=f"mensagem:user:{request.user.pk}",
        limite=MENSAGEM_LIMITE_USUARIO,
        janela_segundos=MENSAGEM_JANELA_SEGUNDOS,
    )
    if not resultado.permitido:
        return resposta_limite_excedido(
            request,
            resultado,
            "Você enviou muitas mensagens em pouco tempo. Aguarde e tente novamente.",
            titulo="Envio de mensagens temporariamente bloqueado",
            voltar_url=reverse("favoritos:interesses"),
        )

    form = LeadMensagemForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Escreva uma mensagem válida de até 1.500 caracteres.")
        return redirect(f"{reverse('favoritos:interesses')}#lead-{lead.id}")

    try:
        responder_como_interessado(
            lead=lead,
            interessado=request.user,
            texto=form.cleaned_data["mensagem"],
        )
    except (ValidationError, PermissionDenied) as exc:
        texto = getattr(exc, "messages", None)
        messages.error(request, texto[0] if texto else str(exc))
    else:
        messages.success(request, "Mensagem enviada ao anunciante.")

    return redirect(f"{reverse('favoritos:interesses')}#lead-{lead.id}")
