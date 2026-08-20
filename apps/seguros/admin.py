from django import forms
from django.contrib import admin

from apps.empresas.models import Empresa

from .models import CotacaoSeguro, Seguro


class SeguroAdminForm(forms.ModelForm):
    class Meta:
        model = Seguro
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        empresa = cleaned_data.get('empresa')

        # RN05: Somente empresas de categoria seguradora ou corretora podem
        # oferecer seguros.
        if empresa and empresa.tipo_empresa not in (
            Empresa.TipoEmpresa.SEGURADORA,
            Empresa.TipoEmpresa.CORRETORA,
        ):
            raise forms.ValidationError(
                "Somente empresas do tipo Seguradora ou Corretora podem "
                "oferecer planos de seguro."
            )

        return cleaned_data


@admin.register(Seguro)
class SeguroAdmin(admin.ModelAdmin):
    form = SeguroAdminForm
    list_display = ('nome', 'empresa', 'valor_referencia')
    list_filter = ('empresa',)
    search_fields = ('nome', 'empresa__nome_fantasia')


@admin.register(CotacaoSeguro)
class CotacaoSeguroAdmin(admin.ModelAdmin):
    list_display = ('comprador', 'veiculo', 'seguro', 'status', 'data_solicitacao')
    list_filter = ('status',)
    search_fields = ('comprador__email', 'veiculo__placa', 'seguro__nome')
