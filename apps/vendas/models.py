from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.veiculos.models import Veiculo


class Venda(BaseModel):
    class StatusVenda(models.TextChoices):
        PENDENTE = "PENDENTE", "Proposta Pendente"
        EM_NEGOCIACAO = "EM_NEGOCIACAO", "Em Negociação"
        CONCLUIDA = "CONCLUIDA", "Venda Concluída"
        CANCELADA = "CANCELADA", "Cancelada/Recusada"

    comprador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="compras")
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name="negociacoes")
    valor_proposta = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=StatusVenda.choices, default=StatusVenda.PENDENTE)
    data_proposta = models.DateTimeField(auto_now_add=True)

    # A lógica de negócio (atualizar Veiculo, criar HistoricoVeiculo) foi
    # movida para apps/vendas/services.py. O save() aqui volta a ser só
    # "salvar o registro" — sem efeitos colaterais escondidos em outros
    # models. Veja services.py para criar_proposta / iniciar_negociacao /
    # concluir_venda / cancelar_venda.

    def __str__(self):
        return f"Proposta de {self.comprador.email} para {self.veiculo.placa}"