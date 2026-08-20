from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.empresas.models import Empresa
from apps.veiculos.models import Veiculo


class Seguro(BaseModel):
    """
    Plano de seguro oferecido por uma seguradora/corretora (Seção 9 da
    documentação técnica: Empresa 1─N Seguro). É um item de catálogo — o
    valor aqui é uma referência; o valor real de cada negociação fica em
    CotacaoSeguro, abaixo.
    """

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="seguros"
    )

    nome = models.CharField(max_length=150)  # Ex.: "Seguro Total", "Seguro Terceiros"
    descricao = models.TextField(blank=True)
    valor_referencia = models.DecimalField(max_digits=10, decimal_places=2)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome_fantasia}"


class CotacaoSeguro(BaseModel):
    """
    Pedido de cotação de um comprador para um plano de seguro, aplicado a um
    veículo específico (Seção 9: Veiculo 1─N CotacaoSeguro). Os campos
    exatos não estão detalhados na documentação — modelados aqui seguindo o
    mesmo padrão do fluxo de Lead (Seção 10.5): pedido registrado, depois
    acompanhado por status até ser respondido.
    """

    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        RESPONDIDA = "RESPONDIDA", "Respondida"
        RECUSADA = "RECUSADA", "Recusada"

    # POST /api/cotacoes/ na Seção 14.2 exige perfil "Comprador" (autenticado),
    # diferente do Lead — por isso aqui o comprador NÃO é opcional.
    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cotacoes_seguro"
    )

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        related_name="cotacoes_seguro"
    )

    seguro = models.ForeignKey(
        Seguro,
        on_delete=models.PROTECT,
        related_name="cotacoes"
    )

    mensagem = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE
    )

    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cotação de {self.comprador.email} - {self.seguro.nome}"
