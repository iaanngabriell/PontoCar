from django.db import models
from django.conf import settings # Importante para ligar a empresa ao Usuário!

class Empresa(models.Model):
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
        on_delete=models.CASCADE, # Se o usuário for apagado, as empresas dele também serão.
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

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome_fantasia} - {self.get_tipo_empresa_display()}"


class Localizacao(models.Model):
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
    estado = models.CharField(max_length=2) # Ex: TO, SP, RJ

    def __str__(self):
        return f"{self.cidade}/{self.estado} - {self.empresa.nome_fantasia}"