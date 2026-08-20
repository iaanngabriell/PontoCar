from django import forms
from django.contrib import admin

from .models import Servico


class ServicoAdminForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        empresa = cleaned_data.get('empresa')

        # RN04: Somente empresas ativas podem oferecer serviços.
        if empresa and not empresa.ativa:
            raise forms.ValidationError(
                "Esta empresa está inativa e não pode oferecer serviços."
            )

        return cleaned_data


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    form = ServicoAdminForm
    list_display = ('nome', 'empresa', 'preco', 'duracao_estimada')
    list_filter = ('empresa',)
    search_fields = ('nome', 'empresa__nome_fantasia')
