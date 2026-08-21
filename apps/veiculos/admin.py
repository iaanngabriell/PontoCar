from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

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


@admin.register(HistoricoVeiculo)
class HistoricoVeiculoAdmin(admin.ModelAdmin):
    list_display = ("veiculo", "motivo", "dono_anterior", "novo_dono", "data_evento")
    list_filter = ("motivo",)
    search_fields = ("veiculo__placa",)