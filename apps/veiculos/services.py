from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Veiculo


@transaction.atomic
def enviar_para_analise(*, veiculo):
    """RASCUNHO -> EM_ANALISE. Vendedor pede a publicação do anúncio."""
    if veiculo.status != Veiculo.StatusVeiculo.RASCUNHO:
        raise ValidationError("Só é possível enviar para análise um anúncio em rascunho.")
    veiculo.status = Veiculo.StatusVeiculo.EM_ANALISE
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def aprovar_veiculo(*, veiculo):
    """EM_ANALISE -> DISPONIVEL. Ação de moderação (RN: pode_moderar_veiculo)."""
    if veiculo.status != Veiculo.StatusVeiculo.EM_ANALISE:
        raise ValidationError("Só é possível aprovar um anúncio em análise.")
    veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def rejeitar_veiculo(*, veiculo):
    """EM_ANALISE -> REJEITADO. Ação de moderação (RN: pode_moderar_veiculo)."""
    if veiculo.status != Veiculo.StatusVeiculo.EM_ANALISE:
        raise ValidationError("Só é possível rejeitar um anúncio em análise.")
    veiculo.status = Veiculo.StatusVeiculo.REJEITADO
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def reenviar_para_analise(*, veiculo):
    """REJEITADO -> EM_ANALISE. Vendedor corrige e reenvia o anúncio."""
    if veiculo.status != Veiculo.StatusVeiculo.REJEITADO:
        raise ValidationError("Só é possível reenviar um anúncio rejeitado.")
    veiculo.status = Veiculo.StatusVeiculo.EM_ANALISE
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def reservar_veiculo(*, veiculo):
    """DISPONIVEL -> RESERVADO. Usado ao abrir uma negociação (vendas.criar_proposta)."""
    if veiculo.status != Veiculo.StatusVeiculo.DISPONIVEL:
        raise ValidationError("Só é possível reservar um veículo disponível.")
    veiculo.status = Veiculo.StatusVeiculo.RESERVADO
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def liberar_veiculo(*, veiculo):
    """RESERVADO -> DISPONIVEL. Usado ao cancelar uma negociação."""
    if veiculo.status != Veiculo.StatusVeiculo.RESERVADO:
        raise ValidationError("Só é possível liberar um veículo reservado.")
    veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def marcar_vendido(*, veiculo):
    """DISPONIVEL ou RESERVADO -> VENDIDO. Usado ao concluir uma venda."""
    if veiculo.status not in (
        Veiculo.StatusVeiculo.DISPONIVEL,
        Veiculo.StatusVeiculo.RESERVADO,
    ):
        raise ValidationError("Só é possível vender um veículo disponível ou reservado.")
    veiculo.status = Veiculo.StatusVeiculo.VENDIDO
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def reativar_veiculo(*, veiculo):
    """VENDIDO ou PAUSADO -> DISPONIVEL. Dono reativa o anúncio manualmente."""
    if veiculo.status not in (
        Veiculo.StatusVeiculo.VENDIDO,
        Veiculo.StatusVeiculo.PAUSADO,
    ):
        raise ValidationError("Só é possível reativar um veículo vendido ou pausado.")
    veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def pausar_veiculo(*, veiculo):
    """DISPONIVEL -> PAUSADO."""
    if veiculo.status != Veiculo.StatusVeiculo.DISPONIVEL:
        raise ValidationError("Só é possível pausar um veículo disponível.")
    veiculo.status = Veiculo.StatusVeiculo.PAUSADO
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def arquivar_veiculo(*, veiculo):
    """PAUSADO -> ARQUIVADO. Manual ou via command da Seção 16.1 (90 dias pausado)."""
    if veiculo.status != Veiculo.StatusVeiculo.PAUSADO:
        raise ValidationError("Só é possível arquivar um veículo pausado.")
    veiculo.status = Veiculo.StatusVeiculo.ARQUIVADO
    veiculo.save(update_fields=["status"])
    return veiculo