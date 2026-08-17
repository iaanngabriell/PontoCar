from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.veiculos.models import Veiculo, HistoricoVeiculo


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

    # A MÁGICA DA AUTOMAÇÃO ACONTECE AQUI
    def save(self, *args, **kwargs):
        # 1. Se alguém faz uma proposta, o carro fica com status "Pendente" (reservado)
        if self.status in [self.StatusVenda.PENDENTE, self.StatusVenda.EM_NEGOCIACAO]:
            if self.veiculo.status != Veiculo.StatusVeiculo.PENDENTE:
                self.veiculo.status = Veiculo.StatusVeiculo.PENDENTE
                self.veiculo.save()

        # 2. Se a venda for concluída DENTRO do site!
        elif self.status == self.StatusVenda.CONCLUIDA:
            # Regista o histórico
            HistoricoVeiculo.objects.create(
                veiculo=self.veiculo,
                dono_anterior=self.veiculo.proprietario_atual,
                novo_dono=self.comprador,
                motivo=HistoricoVeiculo.MotivoEvento.VENDA_SITE,
                mensagem_automatica=f"Quantidade proprietários: {self.veiculo.quantidade_proprietarios + 1} | Proprietário atual: {self.comprador.username or self.comprador.first_name}"
            )

            # Atualiza os dados do veículo
            self.veiculo.proprietario_atual = self.comprador
            self.veiculo.quantidade_proprietarios += 1
            self.veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL  # O carro volta a estar disponível na garagem do novo dono
            self.veiculo.save()

        # 3. Se a venda for cancelada, liberta o carro para outros comprarem
        elif self.status == self.StatusVenda.CANCELADA:
            if self.veiculo.status == Veiculo.StatusVeiculo.PENDENTE:
                self.veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL
                self.veiculo.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Proposta de {self.comprador.email} para {self.veiculo.placa}"
