from decimal import Decimal

from django import forms

from apps.core.form_fields import MoedaBRField

from .models import Servico


class ServicoForm(forms.ModelForm):
    preco = MoedaBRField(
        label="Preço (R$)",
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),
        help_text="Valor de referência exibido no catálogo público.",
        widget=forms.TextInput(attrs={"placeholder": "150,00"}),
    )

    class Meta:
        model = Servico
        fields = ("nome", "descricao", "preco", "duracao_estimada")
        labels = {
            "nome": "Nome do serviço",
            "descricao": "Descrição",
            "duracao_estimada": "Duração estimada (minutos)",
        }
        widgets = {
            "nome": forms.TextInput(attrs={"placeholder": "Ex.: Troca de óleo e filtro"}),
            "descricao": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Descreva o que está incluído no serviço.",
                }
            ),
            "duracao_estimada": forms.NumberInput(
                attrs={"min": "1", "step": "1", "placeholder": "60"}
            ),
        }
        help_texts = {
            "descricao": "Informe os principais itens incluídos no serviço.",
            "duracao_estimada": "Tempo aproximado. O PontoCar não agenda horários neste MVP.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_duracao_estimada(self):
        duracao = self.cleaned_data["duracao_estimada"]
        if duracao <= 0:
            raise forms.ValidationError("Informe uma duração maior que zero.")
        return duracao
