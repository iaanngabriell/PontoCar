from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import BaseModel
from apps.veiculos.models import Veiculo


class Lead(BaseModel):
    """Manifestação de interesse vinculada a um anúncio de veículo."""

    class Status(models.TextChoices):
        NOVO = "NOVO", "Novo"
        CONTATADO = "CONTATADO", "Contatado"
        NEGOCIANDO = "NEGOCIANDO", "Negociando"
        CONVERTIDO = "CONVERTIDO", "Convertido"
        PERDIDO = "PERDIDO", "Perdido"

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        related_name="leads",
    )
    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads_criados",
    )
    # Mantém o anunciante do momento em que o interesse foi criado.
    # Isso evita perder a conversa se o veículo trocar de proprietário depois.
    anunciante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads_recebidos",
    )

    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    mensagem = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOVO,
    )

    # Mantidos por compatibilidade com telas/dados anteriores.
    # Representam apenas a resposta mais recente do anunciante.
    resposta_anunciante = models.TextField(blank=True)
    data_resposta = models.DateTimeField(null=True, blank=True)

    data_criacao = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if not self.comprador_id:
            return

        anunciante_id = self.anunciante_id
        if not anunciante_id and self.veiculo_id:
            anunciante_id = self.veiculo.proprietario_atual_id

        if anunciante_id == self.comprador_id:
            raise ValidationError(
                {"comprador": "O proprietário não pode demonstrar interesse no próprio anúncio."}
            )

    def __str__(self):
        return f"Lead de {self.nome} - {self.veiculo.placa}"


class MensagemLead(BaseModel):
    """Uma mensagem da conversa entre interessado e anunciante."""

    class TipoAutor(models.TextChoices):
        INTERESSADO = "INTERESSADO", "Interessado"
        ANUNCIANTE = "ANUNCIANTE", "Anunciante"

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name="mensagens",
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mensagens_lead",
    )
    tipo_autor = models.CharField(max_length=20, choices=TipoAutor.choices)
    texto = models.TextField(max_length=1500)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("criada_em", "id")

    def __str__(self):
        return f"{self.get_tipo_autor_display()} - {self.lead_id}"
