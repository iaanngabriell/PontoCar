from pathlib import Path

from django import forms

from .models import Empresa, Localizacao


class EmpresaForm(forms.ModelForm):
    cnpj = forms.CharField(
        label="CNPJ",
        max_length=18,
        widget=forms.TextInput(
            attrs={
                "placeholder": "00.000.000/0000-00",
                "inputmode": "numeric",
                "data-mask": "cnpj",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = Empresa
        fields = (
            "razao_social",
            "nome_fantasia",
            "cnpj",
            "tipo_empresa",
            "telefone",
            "email",
        )
        labels = {
            "razao_social": "Razão social",
            "nome_fantasia": "Nome fantasia",
            "cnpj": "CNPJ",
            "tipo_empresa": "Categoria",
            "telefone": "Telefone / WhatsApp",
            "email": "E-mail comercial",
        }
        widgets = {
            "razao_social": forms.TextInput(attrs={"placeholder": "Razão social registrada"}),
            "nome_fantasia": forms.TextInput(attrs={"placeholder": "Nome exibido no PontoCar"}),
            "telefone": forms.TextInput(
                attrs={
                    "placeholder": "(63) 99999-9999",
                    "inputmode": "tel",
                    "data-mask": "telefone",
                    "autocomplete": "tel",
                }
            ),
            "email": forms.EmailInput(attrs={"placeholder": "contato@empresa.com.br", "autocomplete": "email"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_cnpj(self):
        cnpj = "".join(ch for ch in self.cleaned_data["cnpj"] if ch.isdigit())
        if len(cnpj) != 14:
            raise forms.ValidationError("Informe um CNPJ com 14 dígitos.")

        qs = Empresa.objects.filter(cnpj=cnpj)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Já existe uma empresa cadastrada com este CNPJ.")
        return cnpj

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class LocalizacaoForm(forms.ModelForm):
    class Meta:
        model = Localizacao
        fields = ("cep", "logradouro", "numero", "complemento", "bairro", "cidade", "estado")
        labels = {
            "cep": "CEP",
            "logradouro": "Endereço",
            "numero": "Número",
            "complemento": "Complemento",
            "bairro": "Bairro",
            "cidade": "Cidade",
            "estado": "Estado",
        }
        widgets = {
            "cep": forms.TextInput(
                attrs={"placeholder": "77000-000", "inputmode": "numeric", "data-mask": "cep", "autocomplete": "postal-code"}
            ),
            "logradouro": forms.TextInput(attrs={"placeholder": "Avenida, rua, quadra...", "autocomplete": "street-address"}),
            "numero": forms.TextInput(attrs={"placeholder": "Número"}),
            "complemento": forms.TextInput(attrs={"placeholder": "Sala, lote, referência (opcional)"}),
            "bairro": forms.TextInput(attrs={"placeholder": "Bairro"}),
            "cidade": forms.TextInput(attrs={"placeholder": "Palmas", "autocomplete": "address-level2"}),
            "estado": forms.TextInput(
                attrs={"placeholder": "TO", "maxlength": "2", "data-uppercase": "true", "autocomplete": "address-level1"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_cep(self):
        digits = "".join(ch for ch in self.cleaned_data["cep"] if ch.isdigit())
        if len(digits) != 8:
            raise forms.ValidationError("Informe um CEP com 8 dígitos.")
        return f"{digits[:5]}-{digits[5:]}"

    def clean_estado(self):
        estado = self.cleaned_data["estado"].strip().upper()
        if len(estado) != 2 or not estado.isalpha():
            raise forms.ValidationError("Informe a sigla do estado com 2 letras, por exemplo TO.")
        return estado


class VerificacaoEmpresaUploadForm(forms.Form):
    nome_documento = forms.CharField(label="Nome do documento", max_length=150)
    arquivo = forms.FileField(label="Arquivo")
    observacao = forms.CharField(
        label="Observação",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields["arquivo"].widget.attrs["accept"] = ".pdf,.jpg,.jpeg,.png"

    def clean_arquivo(self):
        arquivo = self.cleaned_data["arquivo"]
        if arquivo.size > 8 * 1024 * 1024:
            raise forms.ValidationError("O arquivo deve ter no máximo 8 MB.")
        extensao = Path(arquivo.name).suffix.lower()
        if extensao not in {".pdf", ".jpg", ".jpeg", ".png"}:
            raise forms.ValidationError("Envie um arquivo PDF, JPG ou PNG.")
        return arquivo
