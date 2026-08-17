from django import forms
from django.contrib import admin

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

        # RN11: comprador e proprietário atual não podem ser a mesma pessoa.
        # Validado aqui (no form) para que o admin exiba uma mensagem de erro
        # amigável em vez de estourar o ValidationError levantado dentro de
        # services.criar_proposta().
        if comprador and veiculo and veiculo.proprietario_atual is not None:
            if comprador == veiculo.proprietario_atual:
                raise forms.ValidationError(
                    "O comprador não pode ser o proprietário atual do veículo."
                )

        return cleaned_data


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    form = VendaAdminForm
    list_display = ('veiculo', 'comprador', 'valor_proposta', 'status', 'data_proposta')
    list_filter = ('status', 'data_proposta')
    search_fields = ('veiculo__placa', 'comprador__email')

    # O status não é mais editável direto no formulário: mudar o status
    # dispara efeitos colaterais em outro model (Veiculo, HistoricoVeiculo),
    # então essa transição passa pelas ações abaixo, que usam services.py.
    readonly_fields = ('status',)

    actions = ['acao_iniciar_negociacao', 'acao_concluir_venda', 'acao_cancelar_venda']

    def save_model(self, request, obj, form, change):
        if not change:
            # Criação pelo admin: usa o service para já reservar o veículo
            # corretamente (equivalente ao antigo comportamento do save()).
            # A validação de comprador == proprietário já foi feita no
            # form.clean() acima, mas o services.py mantém o mesmo check
            # como segunda camada de defesa para outros pontos de entrada.
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