from django.urls import reverse

from .models import Notificacao


def criar_notificacao(*, usuario, tipo, titulo, mensagem, chave, url=""):
    """Cria uma notificação idempotente para um evento do domínio."""
    if usuario is None:
        return None

    notificacao, _ = Notificacao.objects.get_or_create(
        chave=chave,
        defaults={
            "usuario": usuario,
            "tipo": tipo,
            "titulo": titulo,
            "mensagem": mensagem,
            "url": url,
        },
    )
    return notificacao


def notificar_novo_interesse(*, lead):
    """Avisa o proprietário atual quando um novo Lead é criado."""
    destinatario = lead.veiculo.proprietario_atual
    if destinatario is None:
        return None

    if lead.comprador_id and lead.comprador_id == destinatario.id:
        return None

    nome = lead.nome.strip() or "Uma pessoa"
    veiculo = f"{lead.veiculo.marca} {lead.veiculo.modelo}".strip()
    return criar_notificacao(
        usuario=destinatario,
        tipo=Notificacao.Tipo.NOVO_INTERESSE,
        titulo=f"Novo interesse em {veiculo}",
        mensagem=f"{nome} demonstrou interesse no seu anúncio.",
        chave=f"lead:{lead.id}:novo",
        url=reverse("leads:vendedor_leads"),
    )


def notificar_nova_proposta(*, venda):
    """Avisa o proprietário do veículo quando uma Venda PENDENTE é criada."""
    destinatario = venda.veiculo.proprietario_atual
    if destinatario is None or destinatario.id == venda.comprador_id:
        return None

    veiculo = f"{venda.veiculo.marca} {venda.veiculo.modelo}".strip()
    return criar_notificacao(
        usuario=destinatario,
        tipo=Notificacao.Tipo.NOVA_PROPOSTA,
        titulo=f"Nova proposta para {veiculo}",
        mensagem=f"{venda.comprador.get_full_name() or venda.comprador.email} enviou uma proposta de compra.",
        chave=f"venda:{venda.id}:pendente",
        url=reverse("notificacoes:lista"),
    )


def notificar_status_proposta(*, venda):
    """Avisa o comprador quando o status da proposta formal muda."""
    rotulos = {
        "EM_NEGOCIACAO": (
            "Sua proposta entrou em negociação",
            "O anunciante iniciou a negociação da sua proposta.",
        ),
        "CONCLUIDA": (
            "Compra concluída",
            "A venda foi concluída e o histórico do veículo foi atualizado.",
        ),
        "CANCELADA": (
            "Proposta encerrada",
            "A proposta foi cancelada ou recusada.",
        ),
    }
    dados = rotulos.get(venda.status)
    if not dados:
        return None

    titulo, mensagem = dados
    veiculo = f"{venda.veiculo.marca} {venda.veiculo.modelo}".strip()
    if venda.status == "CONCLUIDA":
        url = reverse("vendas:comprador_compras")
    else:
        url = reverse("notificacoes:lista")

    return criar_notificacao(
        usuario=venda.comprador,
        tipo=Notificacao.Tipo.PROPOSTA_ATUALIZADA,
        titulo=titulo,
        mensagem=f"{veiculo}: {mensagem}",
        chave=f"venda:{venda.id}:{venda.status.lower()}",
        url=url,
    )
