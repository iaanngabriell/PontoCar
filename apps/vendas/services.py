from django.core.exceptions import ValidationError
from django.db import transaction

from apps.veiculos.models import HistoricoVeiculo, Veiculo

from .models import Venda

@transaction.atomic
def criar_proposta(*, comprador, veiculo, valor_proposta):
    """
    Registra uma nova proposta de compra e reserva o veículo (status PENDENTE).

    Substitui a criação direta de Venda.objects.create(...) quando a intenção
    é abrir uma negociação de verdade (garante RN11: comprador e proprietário
    atual não podem ser a mesma pessoa).
    """
    if veiculo.proprietario_atual is not None and comprador == veiculo.proprietario_atual:
        raise ValidationError("O comprador não pode ser o proprietário atual do veículo.")

    venda = Venda.objects.create(
        comprador=comprador,
        veiculo=veiculo,
        valor_proposta=valor_proposta,
        status=Venda.StatusVenda.PENDENTE,
    )

    if veiculo.status != Veiculo.StatusVeiculo.PENDENTE:
        veiculo.status = Veiculo.StatusVeiculo.PENDENTE
        veiculo.save(update_fields=["status"])

    return venda


@transaction.atomic
def iniciar_negociacao(*, venda):
    """Move a proposta para 'Em Negociação'. O veículo já está reservado."""
    venda.status = Venda.StatusVenda.EM_NEGOCIACAO
    venda.save(update_fields=["status"])
    return venda


@transaction.atomic
def concluir_venda(*, venda):
    """
    Conclui a venda: registra o histórico, transfere a propriedade do veículo
    e o deixa disponível novamente (na garagem do novo dono).
    """
    veiculo = venda.veiculo
    comprador = venda.comprador

    HistoricoVeiculo.objects.create(
        veiculo=veiculo,
        dono_anterior=veiculo.proprietario_atual,
        novo_dono=comprador,
        motivo=HistoricoVeiculo.MotivoEvento.VENDA_SITE,
        mensagem_automatica=(
            f"Quantidade proprietários: {veiculo.quantidade_proprietarios + 1} | "
            f"Proprietário atual: {comprador.username or comprador.first_name}"
        ),
    )

    veiculo.proprietario_atual = comprador
    veiculo.quantidade_proprietarios += 1
    veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL
    veiculo.save(update_fields=["proprietario_atual", "quantidade_proprietarios", "status"])

    venda.status = Venda.StatusVenda.CONCLUIDA
    venda.save(update_fields=["status"])

    return venda


@transaction.atomic
def cancelar_venda(*, venda):
    """Cancela a proposta e libera o veículo, se ele estava reservado por ela."""
    veiculo = venda.veiculo

    if veiculo.status == Veiculo.StatusVeiculo.PENDENTE:
        veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL
        veiculo.save(update_fields=["status"])

    venda.status = Venda.StatusVenda.CANCELADA
    venda.save(update_fields=["status"])
