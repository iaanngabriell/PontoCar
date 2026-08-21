from django import forms
from django.contrib import admin

from apps.empresas.models import Empresa

from .models import ApoliceSeguro, Seguro


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
    list_display = ('nome', 'empresa', 'valor_referencia', 'ativo')
    list_filter = ('ativo', 'empresa')
    search_fields = ('nome', 'empresa__nome_fantasia')


@admin.register(ApoliceSeguro)
class ApoliceSeguroAdmin(admin.ModelAdmin):
    # Não precisa de form customizado para a RN05: o seguro já só pode ter
    # sido criado com uma empresa seguradora/corretora (validado no
    # SeguroAdminForm acima), então qualquer ApoliceSeguro que referencia
    # um Seguro válido já respeita a regra por transitividade.
    list_display = (
        'veiculo', 'contratante', 'seguro',
        'valor_mensal', 'inicio_vigencia', 'fim_vigencia', 'status',
    )
    list_filter = ('status',)
    search_fields = ('veiculo__placa', 'contratante__email', 'seguro__nome')
    readonly_fields = ('esta_ativa',)