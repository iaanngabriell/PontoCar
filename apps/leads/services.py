from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from apps.notificacoes.services import (
    notificar_mensagem_interesse,
    notificar_novo_interesse,
)

from .models import Lead, MensagemLead


def _validar_texto(texto):
    texto = (texto or "").strip()
    if not texto:
        raise ValidationError("Escreva uma mensagem antes de enviar.")
    if len(texto) > 1500:
        raise ValidationError("A mensagem deve ter no máximo 1.500 caracteres.")
    return texto


@transaction.atomic
def registrar_interesse(*, veiculo, comprador, dados):
    """Cria um Lead, registra a primeira mensagem e impede auto-interesse."""
    anunciante = veiculo.proprietario_atual
    if anunciante is None:
        raise ValidationError("Este anúncio não possui um responsável disponível para receber interesses.")

    if comprador is not None and anunciante.id == comprador.id:
        raise ValidationError("Você não pode enviar interesse para o seu próprio anúncio.")

    lead = Lead.objects.create(
        veiculo=veiculo,
        comprador=comprador,
        anunciante=anunciante,
        nome=dados["nome"],
        email=dados["email"],
        telefone=dados["telefone"],
        mensagem=dados.get("mensagem", ""),
        status=Lead.Status.NOVO,
    )

    texto_inicial = (lead.mensagem or "").strip()
    if texto_inicial:
        MensagemLead.objects.create(
            lead=lead,
            autor=comprador,
            tipo_autor=MensagemLead.TipoAutor.INTERESSADO,
            texto=texto_inicial,
        )

    notificar_novo_interesse(lead=lead)
    return lead


@transaction.atomic
def responder_interesse(*, lead, anunciante, resposta, status):
    """Adiciona mensagem do anunciante e atualiza o estágio comercial do Lead."""
    responsavel_id = lead.anunciante_id or lead.veiculo.proprietario_atual_id
    if responsavel_id != anunciante.id:
        raise PermissionDenied("Somente o anunciante responsável pode responder este interesse.")

    permitidos = {
        Lead.Status.NOVO: {
            Lead.Status.CONTATADO,
            Lead.Status.NEGOCIANDO,
            Lead.Status.CONVERTIDO,
            Lead.Status.PERDIDO,
        },
        Lead.Status.CONTATADO: {
            Lead.Status.CONTATADO,
            Lead.Status.NEGOCIANDO,
            Lead.Status.CONVERTIDO,
            Lead.Status.PERDIDO,
        },
        Lead.Status.NEGOCIANDO: {
            Lead.Status.NEGOCIANDO,
            Lead.Status.CONVERTIDO,
            Lead.Status.PERDIDO,
        },
        Lead.Status.CONVERTIDO: {Lead.Status.CONVERTIDO},
        Lead.Status.PERDIDO: {Lead.Status.PERDIDO},
    }.get(lead.status, {lead.status})

    if status not in permitidos:
        raise ValidationError("Essa mudança de etapa do interesse não é permitida.")

    texto = _validar_texto(resposta)
    mensagem = MensagemLead.objects.create(
        lead=lead,
        autor=anunciante,
        tipo_autor=MensagemLead.TipoAutor.ANUNCIANTE,
        texto=texto,
    )

    # Compatibilidade com a versão anterior: mantém a última resposta também
    # nos campos já existentes do Lead.
    lead.resposta_anunciante = texto
    lead.data_resposta = timezone.now()
    lead.status = status
    lead.save(update_fields=["resposta_anunciante", "data_resposta", "status"])

    notificar_mensagem_interesse(mensagem=mensagem)
    return mensagem


@transaction.atomic
def responder_como_interessado(*, lead, interessado, texto):
    """Adiciona uma nova mensagem do usuário que iniciou o interesse."""
    if not lead.comprador_id:
        raise PermissionDenied("Este interesse foi enviado sem uma conta vinculada.")
    if lead.comprador_id != interessado.id:
        raise PermissionDenied("Somente quem enviou o interesse pode responder nesta conversa.")

    texto = _validar_texto(texto)
    mensagem = MensagemLead.objects.create(
        lead=lead,
        autor=interessado,
        tipo_autor=MensagemLead.TipoAutor.INTERESSADO,
        texto=texto,
    )
    notificar_mensagem_interesse(mensagem=mensagem)
    return mensagem
