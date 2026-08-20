from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.veiculos.models import Veiculo


class Lead(BaseModel):
    """
    Manifestação de interesse de um possível comprador em um veículo,
    registrada antes de qualquer proposta de venda formal (Seção 10.5 da
    documentação técnica).
    """

    class Status(models.TextChoices):
        NOVO = "NOVO", "Novo"
        CONTATADO = "CONTATADO", "Contatado"
        NEGOCIANDO = "NEGOCIANDO", "Negociando"
        CONVERTIDO = "CONVERTIDO", "Convertido"
        PERDIDO = "PERDIDO", "Perdido"

    # PROTECT: um lead não pode "sumir" se o veículo for removido — o
    # histórico de interesse precisa ser preservado (mesmo padrão da doc).
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        related_name="leads"
    )

    # Pode ficar nulo: a demonstração de interesse pode vir de um visitante
    # não autenticado (ver Seção 14.2 — POST /api/veiculos/{id}/leads/ é
    # "Público/autenticado"). Por isso nome/email/telefone abaixo são campos
    # de texto livre, não vêm automaticamente do cadastro do usuário.
    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads_criados"
    )

    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    mensagem = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOVO
    )

    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead de {self.nome} - {self.veiculo.placa}"
