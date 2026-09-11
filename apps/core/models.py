import uuid

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    """
    Modelo abstrato base do projeto PontoCar.

    Substitui o BigAutoField padrão do Django por uma chave primária UUID,
    alinhada ao padrão nativo do Supabase (gen_random_uuid()) e à Seção 24
    da documentação técnica. Por ser abstrato, não cria tabela própria —
    cada model que herdar ganha apenas o campo `id` como UUID.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class RateLimitBucket(BaseModel):
    """
    Contador persistente para rate limiting.

    A chave é sempre armazenada como hash SHA-256 pelo helper de rate limit,
    evitando persistir IP, e-mail ou UUID em texto puro nesta tabela.
    """

    chave = models.CharField(max_length=64, unique=True, db_index=True)
    contador = models.PositiveIntegerField(default=0)
    inicio_janela = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "contador de limite de requisições"
        verbose_name_plural = "contadores de limite de requisições"

    def __str__(self):
        return self.chave
