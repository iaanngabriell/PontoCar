from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

from apps.core.rate_limit import (
    consumir_limite,
    obter_ip_cliente,
    resposta_limite_excedido,
)


RECUPERACAO_LIMITE_IP = 6
RECUPERACAO_LIMITE_EMAIL = 3
RECUPERACAO_JANELA_SEGUNDOS = 15 * 60


class RecuperarSenhaForm(PasswordResetForm):
    email = forms.EmailField(
        label="E-mail",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "voce@email.com",
                "autocomplete": "email",
                "autofocus": True,
            }
        ),
    )


class DefinirNovaSenhaForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].label = "Nova senha"
        self.fields["new_password2"].label = "Confirmar nova senha"
        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": "••••••••",
                    "autocomplete": "new-password",
                }
            )


class PasswordResetSeguroView(PasswordResetView):
    template_name = "usuarios/password_reset_form.html"
    email_template_name = "usuarios/password_reset_email.txt"
    subject_template_name = "usuarios/password_reset_subject.txt"
    form_class = RecuperarSenhaForm
    success_url = reverse_lazy("usuarios:password_reset_done")

    def post(self, request, *args, **kwargs):
        ip = obter_ip_cliente(request)
        resultado_ip = consumir_limite(
            chave=f"recuperacao-senha:ip:{ip}",
            limite=RECUPERACAO_LIMITE_IP,
            janela_segundos=RECUPERACAO_JANELA_SEGUNDOS,
        )
        if not resultado_ip.permitido:
            return resposta_limite_excedido(
                request,
                resultado_ip,
                "Muitas solicitações de recuperação de senha. Aguarde e tente novamente.",
                titulo="Recuperação de senha temporariamente bloqueada",
                voltar_url=request.path,
            )

        email = request.POST.get("email", "").strip().lower()
        if email:
            resultado_email = consumir_limite(
                chave=f"recuperacao-senha:email:{email}",
                limite=RECUPERACAO_LIMITE_EMAIL,
                janela_segundos=RECUPERACAO_JANELA_SEGUNDOS,
            )
            if not resultado_email.permitido:
                return resposta_limite_excedido(
                    request,
                    resultado_email,
                    "Muitas solicitações de recuperação de senha. Aguarde e tente novamente.",
                    titulo="Recuperação de senha temporariamente bloqueada",
                    voltar_url=request.path,
                )

        return super().post(request, *args, **kwargs)
