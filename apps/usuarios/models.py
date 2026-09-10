import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):

    # PK trocada de BigAutoField (padrão do AbstractUser) para UUID.
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class TipoUsuario(models.TextChoices):
        COMPRADOR = "COMPRADOR", "Comprador"
        VENDEDOR = "VENDEDOR", "Vendedor"
        EMPRESA = "EMPRESA", "Representante de empresa"
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"

    email = models.EmailField(unique=True)

    cpf = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
    )

    telefone = models.CharField(
        max_length=20,
        blank=True,
    )

    data_nascimento = models.DateField(
        null=True,
        blank=True,
    )

    foto_perfil = models.ImageField(
        upload_to="usuarios/perfis/",
        null=True,
        blank=True,
    )

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.COMPRADOR,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @staticmethod
    def gerar_username(email):
        base = email.split("@")[0]
        username = base
        contador = 1
        while Usuario.objects.filter(username=username).exists():
            username = f"{base}{contador}"
            contador += 1
        return username

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.gerar_username(self.email)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
