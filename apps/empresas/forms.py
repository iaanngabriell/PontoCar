from pathlib import Path

from django import forms

from .models import Empresa, Localizacao


class EmpresaForm(forms.ModelForm):
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
            "telefone": "Telefone",
            "email": "E-mail comercial",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_cnpj(self):
        cnpj = "".join(ch for ch in self.cleaned_data["cnpj"] if ch.isdigit())
        if len(cnpj) != 14:
            raise forms.ValidationError("Informe um CNPJ com 14 dígitos.")
        return cnpj


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


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
