import uuid

from django.db import models


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
