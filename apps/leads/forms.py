from django import forms

from .models import Lead


class LeadMensagemForm(forms.Form):
    mensagem = forms.CharField(
        label="Sua mensagem",
        max_length=1500,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "maxlength": "1500",
                "placeholder": "Escreva sua resposta...",
            }
        ),
    )


class LeadRespostaForm(forms.Form):
    resposta = forms.CharField(
        label="Mensagem ao interessado",
        max_length=1500,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 3,
                "maxlength": "1500",
                "placeholder": "Escreva uma resposta clara para o interessado...",
            }
        ),
    )
    status = forms.ChoiceField(
        label="Etapa do interesse",
        choices=(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    TRANSICOES = {
        Lead.Status.NOVO: {
            Lead.Status.CONTATADO,
            Lead.Status.NEGOCIANDO,
            Lead.Status.CONVERTIDO,
            Lead.Status.PERDIDO,
        },
        Lead.Status.CONTATADO: {
            Lead.Status.CONTATADO,
            Lead.Status.NEGOCIANDO,
            Lead.Status.CONVERTIDO,
            Lead.Status.PERDIDO,
        },
        Lead.Status.NEGOCIANDO: {
            Lead.Status.NEGOCIANDO,
            Lead.Status.CONVERTIDO,
            Lead.Status.PERDIDO,
        },
        Lead.Status.CONVERTIDO: {Lead.Status.CONVERTIDO},
        Lead.Status.PERDIDO: {Lead.Status.PERDIDO},
    }

    def __init__(self, *args, lead, **kwargs):
        super().__init__(*args, **kwargs)
        permitidos = self.TRANSICOES.get(lead.status, {lead.status})
        self.fields["status"].choices = [
            (valor, rotulo)
            for valor, rotulo in Lead.Status.choices
            if valor in permitidos
        ]

        if not self.is_bound:
            if lead.status == Lead.Status.NOVO:
                self.initial.setdefault("status", Lead.Status.CONTATADO)
            else:
                self.initial.setdefault("status", lead.status)
