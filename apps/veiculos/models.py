from django.db import models
from django.conf import settings

class Veiculo(models.Model):
    # Status possíveis do carro na plataforma
    class StatusVeiculo(models.TextChoices):
        DISPONIVEL = "DISPONIVEL", "Disponível"
        RESERVADO = "RESERVADO", "Reservado"
        VENDIDO = "VENDIDO", "Vendido"

    # RELACIONAMENTO: Todo veículo pertence a alguém (vendedor pessoa física ou representante de empresa)
    vendedor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="veiculos"
    )

    marca = models.CharField(max_length=50) 
    modelo = models.CharField(max_length=100)
    ano_fabricacao = models.IntegerField()
    ano_modelo = models.IntegerField()
    
    preco = models.DecimalField(max_digits=10, decimal_places=2) 
    
    quilometragem = models.IntegerField(default=0)
    placa = models.CharField(max_length=7, unique=True)
    cor = models.CharField(max_length=30)
    descricao = models.TextField(blank=True)
    
    status = models.CharField(
        max_length=15,
        choices=StatusVeiculo.choices,
        default=StatusVeiculo.DISPONIVEL
    )

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano_modelo}) - R$ {self.preco}"