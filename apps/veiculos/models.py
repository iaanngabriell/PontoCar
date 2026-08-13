from django.db import models
from django.conf import settings

class Veiculo(models.Model):
    class StatusVeiculo(models.TextChoices):
        DISPONIVEL = "DISPONIVEL", "Disponível"
        PENDENTE = "PENDENTE", "Pendente" # Em negociação
        VENDIDO = "VENDIDO", "Vendido / Inativo" # Quando é vendido ou o anúncio é retirado

    # MUDANÇA: O dono atual pode ser nulo (blank=True, null=True) se o carro for vendido fora do site!
    # Além disso, usamos SET_NULL. Se o dono apagar a conta, o carro não é apagado da base de dados.
    proprietario_atual = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name="veiculos_na_garagem"
    )

    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100)
    ano_fabricacao = models.IntegerField()
    ano_modelo = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quilometragem = models.IntegerField(default=0)
    
    # A Placa/Matrícula é o ID UNIVERSAL do carro no sistema
    placa = models.CharField(max_length=7, unique=True) 
    
    cor = models.CharField(max_length=30)
    descricao = models.TextField(blank=True)
    
    status = models.CharField(
        max_length=15,
        choices=StatusVeiculo.choices,
        default=StatusVeiculo.DISPONIVEL
    )

    # MUDANÇA: Contagem automática de proprietários
    quantidade_proprietarios = models.IntegerField(default=1)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"


class HistoricoVeiculo(models.Model):
    # Opções exatas retiradas da sua documentação!
    class MotivoEvento(models.TextChoices):
        VENDA_SITE = "VENDA_SITE", "Site PontoCar"
        VENDA_LOJA = "VENDA_LOJA", "Venda em loja"
        VENDA_PRESENCIAL = "VENDA_PRESENCIAL", "Venda presencialmente"
        OUTROS = "OUTROS", "Outros"
        ARREPENDIMENTO = "ARREPENDIMENTO", "Arrependi de vender"
        MALSUCEDIDA = "MALSUCEDIDA", "Venda malsucedida"
        CADASTRO = "CADASTRO", "Veículo Cadastrado no Sistema"

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name="historico")
    
    # Registos de quem passou o carro para quem
    dono_anterior = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="historico_vendas")
    novo_dono = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="historico_compras")
    
    motivo = models.CharField(max_length=20, choices=MotivoEvento.choices)
    mensagem_automatica = models.TextField(blank=True) # Ex: "Veículo vendido externamente."
    
    data_evento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Histórico: {self.veiculo.placa} - {self.get_motivo_display()}"