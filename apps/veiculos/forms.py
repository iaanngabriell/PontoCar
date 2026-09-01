import re

from django import forms

from apps.leads.models import Lead

from .models import Veiculo


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = (
            "marca",
            "modelo",
            "versao",
            "ano_fabricacao",
            "ano_modelo",
            "quilometragem",
            "cambio",
            "combustivel",
            "cor",
            "preco",
            "placa",
            "descricao",
        )
        labels = {
            "marca": "Marca",
            "modelo": "Modelo",
            "versao": "Versão",
            "ano_fabricacao": "Ano de fabricação",
            "ano_modelo": "Ano do modelo",
            "quilometragem": "Quilometragem",
            "cambio": "Câmbio",
            "combustivel": "Combustível",
            "cor": "Cor",
            "preco": "Preço (R$)",
            "placa": "Placa",
            "descricao": "Descrição e opcionais",
        }
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_placa(self):
        placa = re.sub(r"[^A-Za-z0-9]", "", self.cleaned_data["placa"]).upper()
        if len(placa) != 7:
            raise forms.ValidationError("Informe uma placa com 7 caracteres.")
        qs = Veiculo.objects.filter(placa=placa)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError(
                "Veículo já cadastrado no sistema. Confira o registro existente antes de continuar."
            )
        return placa


class LeadInteresseForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ("nome", "email", "telefone", "mensagem")
        labels = {
            "nome": "Nome completo",
            "email": "E-mail",
            "telefone": "Telefone / WhatsApp",
            "mensagem": "Mensagem",
        }
        widgets = {
            "mensagem": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["nome"].widget.attrs.setdefault("placeholder", "Seu nome")
        self.fields["email"].widget.attrs.setdefault("placeholder", "voce@email.com")
        self.fields["telefone"].widget.attrs.setdefault("placeholder", "(63) 9 0000-0000")
