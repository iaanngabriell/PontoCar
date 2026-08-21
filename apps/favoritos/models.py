from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.veiculos.models import Veiculo


class Favorito(BaseModel):
    """
    Relação simples de "salvos"/wishlist entre um usuário e um veículo.

    Diferente de Lead: aqui não há contato nenhum com o vendedor, nem
    fluxo de status — é só uma lista pessoal (visto em
    comprador-interesses.html, aba "Favoritos", separada da aba
    "Interesses enviados" que já é o Lead).
    """

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favoritos"
    )

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name="favoritado_por"
    )

    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "veiculo"],
                name="unique_favorito_usuario_veiculo"
            )
        ]

    def __str__(self):
        return f"{self.usuario.email} - {self.veiculo.placa}"
