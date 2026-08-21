from django import forms
from django.contrib import admin

from apps.veiculos.models import Veiculo

from . import services
from .models import Venda


class VendaAdminForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        comprador = cleaned_data.get('comprador')
        veiculo = cleaned_data.get('veiculo')

        if comprador and veiculo:
            # RN11: comprador e proprietário atual não podem ser a mesma pessoa.
            if veiculo.proprietario_atual is not None and comprador == veiculo.proprietario_atual:
                raise forms.ValidationError(
                    "O comprador não pode ser o proprietário atual do veículo."
                )

            # RN13: só é possível propor a compra de um veículo disponível
            # ou já reservado (validado também em services.criar_proposta,
            # mas aqui garante uma mensagem amigável em vez do erro cru).
            if self.instance.pk is None and veiculo.status not in (
                Veiculo.StatusVeiculo.DISPONIVEL,
                Veiculo.StatusVeiculo.RESERVADO,
            ):
                raise forms.ValidationError(
                    f"Este veículo está com status '{veiculo.get_status_display()}' "
                    "e não pode receber uma nova proposta."
                )

        return cleaned_data


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    form = VendaAdminForm
    list_display = ('veiculo', 'comprador', 'valor_proposta', 'status', 'data_proposta')
    list_filter = ('status', 'data_proposta')
    search_fields = ('veiculo__placa', 'comprador__email')

    readonly_fields = ('status',)

    actions = ['acao_iniciar_negociacao', 'acao_concluir_venda', 'acao_cancelar_venda']

    def save_model(self, request, obj, form, change):
        if not change:
            services.criar_proposta(
                comprador=obj.comprador,
                veiculo=obj.veiculo,
                valor_proposta=obj.valor_proposta,
            )
        else:
            super().save_model(request, obj, form, change)

    @admin.action(description="Marcar como Em Negociação")
    def acao_iniciar_negociacao(self, request, queryset):
        for venda in queryset:
            services.iniciar_negociacao(venda=venda)

    @admin.action(description="Concluir venda selecionada")
    def acao_concluir_venda(self, request, queryset):
        for venda in queryset:
            services.concluir_venda(venda=venda)

    @admin.action(description="Cancelar venda selecionada")
    def acao_cancelar_venda(self, request, queryset):
        for venda in queryset:
            services.cancelar_venda(venda=venda)