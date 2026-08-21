from django.contrib import admin
from django.utils import timezone

from .models import Empresa, Localizacao, VerificacaoEmpresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome_fantasia', 'tipo_empresa', 'cnpj', 'representante', 'ativa')
    list_filter = ('tipo_empresa', 'ativa')
    search_fields = ('nome_fantasia', 'cnpj')


@admin.register(Localizacao)
class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'cidade', 'estado', 'cep')


@admin.register(VerificacaoEmpresa)
class VerificacaoEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome_documento', 'empresa', 'status', 'data_envio', 'analisada_por')
    list_filter = ('status',)
    search_fields = ('nome_documento', 'empresa__nome_fantasia')

    # status fica readonly no formulário: a análise passa pelas ações
    # abaixo, que também preenchem analisada_por/analisada_em — evita que
    # alguém troque o status manualmente e esqueça de registrar quem/quando
    # analisou (RN16 depende desses dados para o selo fazer sentido).
    readonly_fields = ('status', 'analisada_por', 'analisada_em')

    actions = ['acao_aprovar', 'acao_rejeitar', 'acao_suspender']

    def _analisar(self, request, queryset, novo_status):
        queryset.update(
            status=novo_status,
            analisada_por=request.user,
            analisada_em=timezone.now(),
        )

    @admin.action(description="Aprovar documento(s) selecionado(s)")
    def acao_aprovar(self, request, queryset):
        self._analisar(request, queryset, VerificacaoEmpresa.Status.APROVADA)

    @admin.action(description="Rejeitar documento(s) selecionado(s)")
    def acao_rejeitar(self, request, queryset):
        self._analisar(request, queryset, VerificacaoEmpresa.Status.REJEITADA)

    @admin.action(description="Suspender verificação selecionada")
    def acao_suspender(self, request, queryset):
        self._analisar(request, queryset, VerificacaoEmpresa.Status.SUSPENSA)