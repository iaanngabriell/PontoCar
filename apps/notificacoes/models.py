from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Notificacao(BaseModel):
    class Tipo(models.TextChoices):
        NOVO_INTERESSE = "NOVO_INTERESSE", "Novo interesse"
        NOVA_PROPOSTA = "NOVA_PROPOSTA", "Nova proposta"
        PROPOSTA_ATUALIZADA = "PROPOSTA_ATUALIZADA", "Proposta atualizada"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificacoes",
    )
    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    titulo = models.CharField(max_length=140)
    mensagem = models.CharField(max_length=280)
    url = models.CharField(max_length=300, blank=True, default="")
    chave = models.CharField(max_length=180, unique=True)
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)
    lida_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-criada_em",)
        indexes = [
            models.Index(fields=("usuario", "lida", "-criada_em"), name="notif_user_lida_idx"),
        ]

    def __str__(self):
        return f"{self.titulo} — {self.usuario}"
