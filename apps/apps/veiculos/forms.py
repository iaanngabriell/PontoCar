import re
from decimal import Decimal

from django import forms

from apps.core.form_fields import MoedaBRField
from apps.leads.models import Lead

from .models import Veiculo


class VeiculoForm(forms.ModelForm):
    preco = MoedaBRField(
        label="Preço",
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),
        help_text="Informe o valor anunciado. Ex.: 128.900,00.",
        widget=forms.TextInput(attrs={"placeholder": "128.900,00"}),
    )

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
            "placa": "Placa",
            "descricao": "Descrição e opcionais",
        }
        widgets = {
            "marca": forms.TextInput(attrs={"placeholder": "Ex.: Toyota", "autocomplete": "off"}),
            "modelo": forms.TextInput(attrs={"placeholder": "Ex.: Corolla", "autocomplete": "off"}),
            "versao": forms.TextInput(attrs={"placeholder": "Ex.: XEi 2.0 Flex", "autocomplete": "off"}),
            "ano_fabricacao": forms.NumberInput(attrs={"min": "1900", "step": "1", "inputmode": "numeric"}),
            "ano_modelo": forms.NumberInput(attrs={"min": "1900", "step": "1", "inputmode": "numeric"}),
            "quilometragem": forms.NumberInput(attrs={"min": "0", "step": "1", "inputmode": "numeric", "placeholder": "34000"}),
            "cor": forms.TextInput(attrs={"placeholder": "Ex.: Prata", "autocomplete": "off"}),
            "placa": forms.TextInput(
                attrs={
                    "placeholder": "ABC1D23",
                    "maxlength": "7",
                    "autocomplete": "off",
                    "autocapitalize": "characters",
                    "spellcheck": "false",
                    "data-uppercase": "true",
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    "rows": 7,
                    "maxlength": "2000",
                    "placeholder": "Descreva conservação, revisões, opcionais, pneus, documentação e outros diferenciais do veículo.",
                    "data-description-counter": "true",
                }
            ),
        }
        help_texts = {
            "placa": "Digite os 7 caracteres. A placa será armazenada em letras maiúsculas e identifica o veículo de forma única.",
            "descricao": "Use este espaço para apresentar o veículo com clareza. Máximo de 2.000 caracteres.",
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

    def clean_quilometragem(self):
        quilometragem = self.cleaned_data["quilometragem"]
        if quilometragem < 0:
            raise forms.ValidationError("A quilometragem não pode ser negativa.")
        return quilometragem


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
