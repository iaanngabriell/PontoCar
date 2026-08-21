from django.core.exceptions import ValidationError
from django.db import transaction

from apps.veiculos import services as veiculos_services
from apps.veiculos.models import HistoricoVeiculo, Veiculo

from .models import Venda

@transaction.atomic
def criar_proposta(*, comprador, veiculo, valor_proposta):
    """
    Registra uma nova proposta de compra e reserva o veículo, se ele
    ainda estiver disponível (RN11 + RN13).
    """
    if veiculo.proprietario_atual is not None and comprador == veiculo.proprietario_atual:
        raise ValidationError("O comprador não pode ser o proprietário atual do veículo.")

    if veiculo.status not in (Veiculo.StatusVeiculo.DISPONIVEL, Veiculo.StatusVeiculo.RESERVADO):
        raise ValidationError(
            "Só é possível propor a compra de um veículo disponível ou já reservado."
        )

    venda = Venda.objects.create(
        comprador=comprador,
        veiculo=veiculo,
        valor_proposta=valor_proposta,
        status=Venda.StatusVenda.PENDENTE,
    )

    if veiculo.status == Veiculo.StatusVeiculo.DISPONIVEL:
        veiculos_services.reservar_veiculo(veiculo=veiculo)

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
    Conclui a venda: registra o histórico, transfere a propriedade do
    veículo e o marca como VENDIDO (o novo dono reativa manualmente se
    quiser revender — ação 'reativar' no admin).
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
    veiculo.save(update_fields=["proprietario_atual", "quantidade_proprietarios"])

    veiculos_services.marcar_vendido(veiculo=veiculo)

    venda.status = Venda.StatusVenda.CONCLUIDA
    venda.save(update_fields=["status"])

    return venda


@transaction.atomic
def cancelar_venda(*, venda):
    """Cancela a proposta e libera o veículo, se ele estava reservado por ela."""
    veiculo = venda.veiculo

    if veiculo.status == Veiculo.StatusVeiculo.RESERVADO:
        veiculos_services.liberar_veiculo(veiculo=veiculo)

    venda.status = Venda.StatusVenda.CANCELADA
    venda.save(update_fields=["status"])