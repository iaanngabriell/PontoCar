from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    
    # As opções do Select
    class TipoUsuario(models.TextChoices):
        COMPRADOR = "COMPRADOR", "Comprador"
        VENDEDOR = "VENDEDOR", "Vendedor"
        EMPRESA = "EMPRESA", "Representante de empresa"
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"

    email = models.EmailField(
        unique=True
    )

    cpf = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True
    )

    telefone = models.CharField(
        max_length=20,
        blank=True # Ótima adição! Torna o telefone opcional nos formulários.
    )

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices, # É isso aqui que gera o <select> no HTML!
        default=TipoUsuario.COMPRADOR
    )

    # Configura o login para ser por e-mail em vez de username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    # Define como o usuário será exibido no painel de administração
    def __str__(self):
        return self.email