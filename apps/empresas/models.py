from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class Empresa(BaseModel):
    class TipoEmpresa(models.TextChoices):
        REVENDA = "REVENDA", "Revenda de Veículos"
        CONCESSIONARIA = "CONCESSIONARIA", "Concessionária Autorizada"
        OFICINA = "OFICINA", "Oficina Mecânica"
        SEGURADORA = "SEGURADORA", "Seguradora"
        CORRETORA = "CORRETORA", "Corretora de Seguros"

    representante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="empresas",
    )

    nome_fantasia = models.CharField(max_length=100)
    razao_social = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField()
    logo = models.ImageField(
        upload_to="empresas/logos/",
        null=True,
        blank=True,
    )

    tipo_empresa = models.CharField(
        max_length=20,
        choices=TipoEmpresa.choices,
        default=TipoEmpresa.REVENDA,
    )

    ativa = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def possui_selo_ativo(self):
        if self.verificacoes.filter(status=VerificacaoEmpresa.Status.SUSPENSA).exists():
            return False
        return self.verificacoes.filter(status=VerificacaoEmpresa.Status.APROVADA).exists()

    def __str__(self):
        return f"{self.nome_fantasia} - {self.get_tipo_empresa_display()}"


class Localizacao(BaseModel):
    empresa = models.OneToOneField(
        Empresa,
        on_delete=models.CASCADE,
        related_name="localizacao",
    )

    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.cidade}/{self.estado} - {self.empresa.nome_fantasia}"


class VerificacaoEmpresa(BaseModel):
    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        APROVADA = "APROVADA", "Aprovada"
        REJEITADA = "REJEITADA", "Rejeitada"
        SUSPENSA = "SUSPENSA", "Suspensa"

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="verificacoes",
    )

    nome_documento = models.CharField(max_length=150)
    caminho_documento = models.CharField(max_length=500)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )

    observacao_solicitante = models.TextField(blank=True)
    observacao_administrador = models.TextField(blank=True)

    analisada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verificacoes_analisadas",
    )

    data_envio = models.DateTimeField(auto_now_add=True)
    analisada_em = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome_documento} - {self.empresa.nome_fantasia} ({self.get_status_display()})"
