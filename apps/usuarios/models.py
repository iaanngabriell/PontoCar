import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Usuário autenticável do PontoCar.

    `tipo_usuario` agora representa o tipo da conta, não o papel de compra/venda.
    Uma conta pessoal pode comprar e vender com a mesma identidade.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class TipoUsuario(models.TextChoices):
        USUARIO = "USUARIO", "Conta pessoal"
        EMPRESA = "EMPRESA", "Conta empresarial"
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
        default=TipoUsuario.USUARIO,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def eh_conta_pessoal(self):
        return self.tipo_usuario == self.TipoUsuario.USUARIO

    @property
    def eh_conta_empresarial(self):
        return self.tipo_usuario == self.TipoUsuario.EMPRESA

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
