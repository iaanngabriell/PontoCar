from django.contrib import admin
from .models import Empresa, Localizacao

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'tipo_empresa', 'cnpj', 'representante', 'ativa')
    list_filter = ('tipo_empresa', 'ativa')
    search_fields = ('nome_fantasia', 'cnpj')

@admin.register(Localizacao)
class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'cidade', 'estado', 'cep')