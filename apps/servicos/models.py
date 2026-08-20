from django.db import models

from apps.core.models import BaseModel
from apps.empresas.models import Empresa


class Servico(BaseModel):
    """
    Catálogo de serviços automotivos oferecidos por uma empresa (Seção
    24.2.5 da documentação técnica). MVP = listagem/consulta apenas, sem
    agendamento de horário — 'duracao_estimada' é só informativo.
    """

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="servicos"
    )

    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    # Em minutos. Informativo apenas — não reserva horário nenhum no MVP.
    duracao_estimada = models.PositiveIntegerField(
        help_text="Duração estimada do serviço, em minutos."
    )

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.empresa.nome_fantasia}"
