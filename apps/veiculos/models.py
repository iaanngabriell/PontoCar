from django.conf import settings
from django.db import models

from apps.core.models import BaseModel

class Veiculo(BaseModel):
    class StatusVeiculo(models.TextChoices):
        RASCUNHO = "RASCUNHO", "Rascunho"
        EM_ANALISE = "EM_ANALISE", "Em Análise"
        DISPONIVEL = "DISPONIVEL", "Disponível"
        RESERVADO = "RESERVADO", "Reservado"
        VENDIDO = "VENDIDO", "Vendido"
        REJEITADO = "REJEITADO", "Rejeitado"
        PAUSADO = "PAUSADO", "Pausado"
        ARQUIVADO = "ARQUIVADO", "Arquivado"

    proprietario_atual = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="veiculos_na_garagem"
    )

    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    versao = models.CharField(max_length=120, blank=True, null=True)
    ano_fabricacao = models.IntegerField()
    ano_modelo = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quilometragem = models.IntegerField(default=0)
    placa = models.CharField(max_length=7, unique=True)
    cor = models.CharField(max_length=30)

    class CombustivelVeiculo(models.TextChoices):
        FLEX = "FLEX", "Flex"
        GASOLINA = "GASOLINA", "Gasolina"
        DIESEL = "DIESEL", "Diesel"
        ELETRICO = "ELETRICO", "Elétrico"
        HIBRIDO = "HIBRIDO", "Híbrido"

    combustivel = models.CharField(
        max_length=20, choices=CombustivelVeiculo.choices, null=True, blank=True,
    )

    class CambioVeiculo(models.TextChoices):
        MANUAL = "MANUAL", "Manual"
        AUTOMATICO = "AUTOMATICO", "Automático"
        CVT = "CVT", "CVT"

    cambio = models.CharField(
        max_length=20, choices=CambioVeiculo.choices, null=True, blank=True,
    )

    descricao = models.TextField(blank=True)

    status = models.CharField(
        max_length=15,
        choices=StatusVeiculo.choices,
        default=StatusVeiculo.DISPONIVEL
    )

    quantidade_proprietarios = models.IntegerField(default=1)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("pode_moderar_veiculo", "Pode aprovar ou rejeitar anúncios de veículo"),
        ]

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

class HistoricoVeiculo(BaseModel):
    class MotivoEvento(models.TextChoices):
        VENDA_SITE = "VENDA_SITE", "Site PontoCar"
        VENDA_LOJA = "VENDA_LOJA", "Venda em loja"
        VENDA_PRESENCIAL = "VENDA_PRESENCIAL", "Venda presencialmente"
        OUTROS = "OUTROS", "Outros"
        ARREPENDIMENTO = "ARREPENDIMENTO", "Arrependi de vender"
        MALSUCEDIDA = "MALSUCEDIDA", "Venda malsucedida"
        CADASTRO = "CADASTRO", "Veículo Cadastrado no Sistema"

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name="historico")
    dono_anterior = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="historico_vendas")
    novo_dono = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="historico_compras")
    motivo = models.CharField(max_length=20, choices=MotivoEvento.choices)
    mensagem_automatica = models.TextField(blank=True)
    data_evento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Histórico: {self.veiculo.placa} - {self.get_motivo_display()}"


def foto_veiculo_upload_path(instance, filename):
    """Salva em media/veiculos/<placa>/<filename>"""
    return f"veiculos/{instance.veiculo.placa}/{filename}"


class FotoVeiculo(BaseModel):
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name="fotos",
    )
    imagem = models.ImageField(upload_to=foto_veiculo_upload_path)
    principal = models.BooleanField(default=False)
    ordem = models.PositiveSmallIntegerField(default=0)
    texto_alternativo = models.CharField(max_length=150, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ordem", "criado_em"]
        constraints = [
            models.UniqueConstraint(
                fields=["veiculo"],
                condition=models.Q(principal=True),
                name="uq_foto_principal_por_veiculo",
            )
        ]

    def __str__(self):
        return f"Foto {'principal' if self.principal else self.ordem} — {self.veiculo.placa}"