from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel


class Seguro(BaseModel):
    """
    Plano de seguro oferecido por uma seguradora/corretora.
    É um item de catálogo — o valor aqui é referência;
    o valor real de cada apólice fica em ApoliceSeguro.
    """

    empresa = models.ForeignKey(
        "empresas.Empresa",
        on_delete=models.CASCADE,
        related_name="seguros",
    )
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    valor_referencia = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} — {self.empresa.nome_fantasia}"


class ApoliceSeguro(BaseModel):
    """
    Apólice ativa criada pela seguradora para um veículo/contratante.
    O valor mensal real pode diferir do valor_referencia do plano.
    """

    class StatusApolice(models.TextChoices):
        ATIVA = "ATIVA", "Ativa"
        EXPIRADA = "EXPIRADA", "Expirada"
        CANCELADA = "CANCELADA", "Cancelada"

    seguro = models.ForeignKey(
        Seguro,
        on_delete=models.PROTECT,
        related_name="apolices",
    )
    veiculo = models.ForeignKey(
        "veiculos.Veiculo",
        on_delete=models.PROTECT,
        related_name="apolices",
    )
    contratante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="apolices",
    )
    valor_mensal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Valor real contratado. Pode diferir do valor_referencia do plano.",
    )
    inicio_vigencia = models.DateField()
    fim_vigencia = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=StatusApolice.choices,
        default=StatusApolice.ATIVA,
    )

    def esta_ativa(self):
        hoje = timezone.now().date()
        return (
            self.status == self.StatusApolice.ATIVA
            and self.inicio_vigencia <= hoje <= self.fim_vigencia
        )

    def __str__(self):
        return (
            f"Apólice {self.veiculo.placa} — "
            f"{self.seguro.nome} ({self.get_status_display()})"
        )