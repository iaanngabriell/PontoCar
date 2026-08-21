from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from . import services
from .models import FotoVeiculo, HistoricoVeiculo, Veiculo

LIMITE_FOTOS = 8


class FotoVeiculoFormSet(BaseInlineFormSet):
    """Impede cadastrar mais de 8 fotos por veículo."""

    def clean(self):
        super().clean()
        total = sum(
            1
            for form in self.forms
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False)
        )
        if total > LIMITE_FOTOS:
            raise ValidationError(
                f"Um veículo pode ter no máximo {LIMITE_FOTOS} fotos."
            )


class FotoVeiculoInline(admin.TabularInline):
    model = FotoVeiculo
    formset = FotoVeiculoFormSet
    extra = 1
    fields = ("imagem", "principal", "ordem", "texto_alternativo")


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    inlines = [FotoVeiculoInline]
    list_display = (
        "placa", "marca", "modelo", "preco", "status",
        "proprietario_atual", "quantidade_proprietarios",
    )
    list_filter = ("status", "marca", "combustivel", "cambio")
    search_fields = ("marca", "modelo", "placa")

    # Status só muda por ação (mesmo padrão do VendaAdmin) — as transições
    # têm regras próprias (RN09) que vivem em services.py.
    readonly_fields = ("status",)

    actions = [
        "acao_enviar_para_analise",
        "acao_aprovar",
        "acao_rejeitar",
        "acao_reenviar_para_analise",
        "acao_pausar",
        "acao_reativar",
        "acao_arquivar",
    ]

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Aprovar/rejeitar são ações de moderação (Seção 8 da doc):
        # visíveis só para quem tem a permissão pode_moderar_veiculo.
        if not request.user.has_perm("veiculos.pode_moderar_veiculo"):
            actions.pop("acao_aprovar", None)
            actions.pop("acao_rejeitar", None)
        return actions

    def _executar_acao(self, request, queryset, func, mensagem_sucesso):
        sucesso = 0
        for veiculo in queryset:
            try:
                func(veiculo=veiculo)
                sucesso += 1
            except ValidationError as e:
                self.message_user(request, f"{veiculo}: {e.message}", level=messages.ERROR)
        if sucesso:
            self.message_user(request, f"{mensagem_sucesso} ({sucesso} veículo(s)).")

    @admin.action(description="Enviar para análise")
    def acao_enviar_para_analise(self, request, queryset):
        self._executar_acao(request, queryset, lambda veiculo: services.enviar_para_analise(veiculo=veiculo), "Enviado(s) para análise")

    @admin.action(description="Aprovar anúncio (moderação)")
    def acao_aprovar(self, request, queryset):
        self._executar_acao(request, queryset, lambda veiculo: services.aprovar_veiculo(veiculo=veiculo), "Aprovado(s)")

    @admin.action(description="Rejeitar anúncio (moderação)")
    def acao_rejeitar(self, request, queryset):
        self._executar_acao(request, queryset, lambda veiculo: services.rejeitar_veiculo(veiculo=veiculo), "Rejeitado(s)")

    @admin.action(description="Reenviar para análise (após rejeição)")
    def acao_reenviar_para_analise(self, request, queryset):
        self._executar_acao(request, queryset, lambda veiculo: services.reenviar_para_analise(veiculo=veiculo), "Reenviado(s) para análise")

    @admin.action(description="Pausar anúncio")
    def acao_pausar(self, request, queryset):
        self._executar_acao(request, queryset, lambda veiculo: services.pausar_veiculo(veiculo=veiculo), "Pausado(s)")

    @admin.action(description="Reativar anúncio")
    def acao_reativar(self, request, queryset):
        self._executar_acao(request, queryset, lambda veiculo: services.reativar_veiculo(veiculo=veiculo), "Reativado(s)")

    @admin.action(description="Arquivar anúncio")
    def acao_arquivar(self, request, queryset):
        self._executar_acao(request, queryset, lambda veiculo: services.arquivar_veiculo(veiculo=veiculo), "Arquivado(s)")


@admin.register(HistoricoVeiculo)
class HistoricoVeiculoAdmin(admin.ModelAdmin):
    list_display = ("veiculo", "motivo", "dono_anterior", "novo_dono", "data_evento")
    list_filter = ("motivo",)
    search_fields = ("veiculo__placa",)