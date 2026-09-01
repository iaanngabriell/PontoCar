from django import forms

from .models import Servico


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ("nome", "descricao", "preco", "duracao_estimada")
        labels = {
            "nome": "Nome do serviço",
            "descricao": "Descrição",
            "preco": "Preço (R$)",
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
            "preco": forms.NumberInput(
                attrs={"min": "0.01", "step": "0.01", "placeholder": "150,00"}
            ),
            "duracao_estimada": forms.NumberInput(
                attrs={"min": "1", "step": "1", "placeholder": "60"}
            ),
        }
        help_texts = {
            "descricao": "Informe os principais itens incluídos no serviço.",
            "preco": "Valor de referência exibido no catálogo público.",
            "duracao_estimada": "Tempo aproximado. O PontoCar não agenda horários neste MVP.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def clean_preco(self):
        preco = self.cleaned_data["preco"]
        if preco <= 0:
            raise forms.ValidationError("Informe um preço maior que zero.")
        return preco

    def clean_duracao_estimada(self):
        duracao = self.cleaned_data["duracao_estimada"]
        if duracao <= 0:
            raise forms.ValidationError("Informe uma duração maior que zero.")
        return duracao
