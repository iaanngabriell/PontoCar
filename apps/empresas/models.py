from django.conf import settings  # Importante para ligar a empresa ao Usuário!
from django.db import models

from apps.core.models import BaseModel


class Empresa(BaseModel):
    # Tipos de empresas conforme a sua documentação
    class TipoEmpresa(models.TextChoices):
        REVENDA = "REVENDA", "Revenda de Veículos"
        CONCESSIONARIA = "CONCESSIONARIA", "Concessionária Autorizada"
        OFICINA = "OFICINA", "Oficina Mecânica"
        SEGURADORA = "SEGURADORA", "Seguradora"
        CORRETORA = "CORRETORA", "Corretora de Seguros"

    # RELACIONAMENTO (N para 1): Várias empresas podem pertencer a um usuário.
    representante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # Se o usuário for apagado, as empresas dele também serão.
        related_name='empresas'
    )

    nome_fantasia = models.CharField(max_length=100)
    razao_social = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField()

    tipo_empresa = models.CharField(
        max_length=20,
        choices=TipoEmpresa.choices,
        default=TipoEmpresa.REVENDA
    )

    # RN04 (servicos) precisa disso para saber quais empresas podem oferecer
    # serviços; RN05 (seguros) usa tipo_empresa acima para restringir a
    # SEGURADORA/CORRETORA. Sem esse campo, RN04 não tinha como ser aplicada.
    ativa = models.BooleanField(default=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def possui_selo_ativo(self):
        """
        RN16: o selo de confiança depende de verificação aprovada e não
        suspensa. Usado em empresa-verificacao.html e admin-empresas.html
        ("Selo de confiança ativo").
        """
        if self.verificacoes.filter(status=VerificacaoEmpresa.Status.SUSPENSA).exists():
            return False
        return self.verificacoes.filter(status=VerificacaoEmpresa.Status.APROVADA).exists()

    def __str__(self):
        return f"{self.nome_fantasia} - {self.get_tipo_empresa_display()}"


class Localizacao(BaseModel):
    # RELACIONAMENTO (1 para 1): Uma empresa tem UM endereço principal.
    empresa = models.OneToOneField(
        Empresa,
        on_delete=models.CASCADE,
        related_name='localizacao'
    )

    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=200)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)  # Ex: TO, SP, RJ

    def __str__(self):
        return f"{self.cidade}/{self.estado} - {self.empresa.nome_fantasia}"


class VerificacaoEmpresa(BaseModel):
    """
    Um registro por documento enviado (Seção 10.7 da doc técnica —
    'caminho_documento' é singular, não uma lista). Bate com
    empresa-verificacao.html, onde cada linha da tabela de "Documentos
    enviados" é um documento com seu próprio status.

    'nome_documento' não está na Seção 10.7, mas é necessário para a tabela
    saber o que exibir em cada linha (ex.: "Cartão CNPJ", "RG do
    responsável legal").
    """

    class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        APROVADA = "APROVADA", "Aprovada"
        REJEITADA = "REJEITADA", "Rejeitada"
        SUSPENSA = "SUSPENSA", "Suspensa"

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="verificacoes"
    )

    nome_documento = models.CharField(max_length=150)
    caminho_documento = models.CharField(max_length=500)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE
    )

    observacao_solicitante = models.TextField(blank=True)
    observacao_administrador = models.TextField(blank=True)

    analisada_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verificacoes_analisadas"
    )

    data_envio = models.DateTimeField(auto_now_add=True)
    analisada_em = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome_documento} - {self.empresa.nome_fantasia} ({self.get_status_display()})"