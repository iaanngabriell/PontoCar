import re
from decimal import Decimal
from uuid import UUID

from django import forms

from apps.core.form_fields import MoedaBRField
from apps.leads.models import Lead

from .models import MarcaVeiculo, ModeloVeiculo, Veiculo


class VeiculoForm(forms.ModelForm):
    marca_catalogo = forms.ModelChoiceField(
        label="Marca",
        queryset=MarcaVeiculo.objects.none(),
        empty_label="Selecione a marca",
        required=True,
    )
    modelo_catalogo = forms.ModelChoiceField(
        label="Modelo (FIPE)",
        queryset=ModeloVeiculo.objects.none(),
        empty_label="Selecione primeiro a marca",
        required=True,
        help_text="Lista padronizada pelo catálogo FIPE para evitar nomes duplicados ou divergentes.",
    )
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
            "marca_catalogo",
            "modelo_catalogo",
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
            "versao": "Complemento da versão (opcional)",
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
            "versao": forms.TextInput(attrs={"placeholder": "Ex.: pacote Premium, série especial", "autocomplete": "off"}),
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

        marcas_ativas = MarcaVeiculo.objects.filter(ativa=True).order_by("nome")
        self.fields["marca_catalogo"].queryset = marcas_ativas
        self.fields["marca_catalogo"].widget.attrs["data-vehicle-brand"] = "true"
        self.fields["modelo_catalogo"].widget.attrs["data-vehicle-model"] = "true"

        marca_id = self.data.get("marca_catalogo") if self.is_bound else None
        marca_inicial = self.instance.marca_catalogo if self.instance and self.instance.pk else None

        # Compatibilidade: ao editar anúncio antigo, tenta reconhecer a marca pelo
        # texto existente e já apresenta o catálogo correspondente.
        if not self.is_bound and self.instance and self.instance.pk and marca_inicial is None:
            marca_inicial = marcas_ativas.filter(nome__iexact=self.instance.marca).first()
            if marca_inicial is None:
                marca_inicial = marcas_ativas.filter(nome_origem__iexact=self.instance.marca).first()
            if marca_inicial is not None:
                self.initial["marca_catalogo"] = marca_inicial.pk

        if marca_id:
            try:
                marca_uuid = UUID(str(marca_id))
            except (ValueError, TypeError, AttributeError):
                marca_uuid = None
            if marca_uuid:
                self.fields["modelo_catalogo"].queryset = ModeloVeiculo.objects.filter(
                    marca_id=marca_uuid,
                    marca__ativa=True,
                    ativo=True,
                ).order_by("nome")
        elif marca_inicial is not None:
            self.fields["modelo_catalogo"].queryset = marca_inicial.modelos.filter(ativo=True).order_by("nome")
            if self.instance.modelo_catalogo_id:
                self.initial["modelo_catalogo"] = self.instance.modelo_catalogo_id
            elif self.instance and self.instance.pk:
                modelo_legado = self.fields["modelo_catalogo"].queryset.filter(
                    nome__iexact=self.instance.modelo
                ).first()
                if modelo_legado:
                    self.initial["modelo_catalogo"] = modelo_legado.pk

        if not marcas_ativas.exists():
            self.fields["marca_catalogo"].help_text = (
                "O catálogo de veículos ainda não foi sincronizado. Execute "
                "`python manage.py sincronizar_catalogo_fipe`."
            )

        for field in self.fields.values():
            classes = field.widget.attrs.get("class", "").split()
            if "form-control" not in classes:
                classes.append("form-control")
            field.widget.attrs["class"] = " ".join(filter(None, classes))

    def clean(self):
        cleaned = super().clean()
        marca = cleaned.get("marca_catalogo")
        modelo = cleaned.get("modelo_catalogo")
        if marca and modelo and modelo.marca_id != marca.id:
            self.add_error("modelo_catalogo", "Selecione um modelo pertencente à marca escolhida.")
        if marca and not marca.ativa:
            self.add_error("marca_catalogo", "Esta marca não está mais ativa no catálogo.")
        if modelo and not modelo.ativo:
            self.add_error("modelo_catalogo", "Este modelo não está mais ativo no catálogo.")
        return cleaned

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
