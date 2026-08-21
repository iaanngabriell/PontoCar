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

    # As opções do Select
    class TipoUsuario(models.TextChoices):
        COMPRADOR = "COMPRADOR", "Comprador"
        VENDEDOR = "VENDEDOR", "Vendedor"
        EMPRESA = "EMPRESA", "Representante de empresa"
        ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
        # PARCEIRO fica de fora por enquanto — entra junto com o app "seguros",
        # quando esse papel passar a ter uso real no sistema.

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
        blank=True  # Ótima adição! Torna o telefone opcional nos formulários.
    )

    data_nascimento = models.DateField(
        null=True,
        blank=True
    )

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,  # É isso aqui que gera o <select> no HTML!
        default=TipoUsuario.COMPRADOR
    )

    # Configura o login para ser por e-mail em vez de username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @staticmethod
    def gerar_username(email):
        """
        Gera um username único a partir do e-mail (parte antes do @).

        O formulário de cadastro do site não pede username — só nome,
        sobrenome, CPF, e-mail, telefone e senha — mas o AbstractUser ainda
        exige esse campo (REQUIRED_FIELDS = ["username"]). Em vez de expor
        isso pro usuário final, geramos automaticamente.

        Ex.: joao.silva@gmail.com -> "joao.silva" (ou "joao.silva1" se já
        existir alguém com esse username).
        """
        base = email.split("@")[0]
        username = base
        contador = 1
        while Usuario.objects.filter(username=username).exists():
            username = f"{base}{contador}"
            contador += 1
        return username

    def save(self, *args, **kwargs):
        # Preenche o username automaticamente sempre que ele não for
        # informado explicitamente (cobre cadastro pelo site, shell, e
        # qualquer outro ponto de criação que não passe username à mão).
        if not self.username:
            self.username = self.gerar_username(self.email)
        super().save(*args, **kwargs)

    # Define como o usuário será exibido no painel de administração
    def __str__(self):
        return self.email