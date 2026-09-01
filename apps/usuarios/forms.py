from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm

from .models import Usuario


class FormControlMixin:
    def aplicar_classes(self):
        for field in self.fields.values():
            css = "form-control"
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                css = ""
            if css:
                field.widget.attrs["class"] = css


class LoginForm(FormControlMixin, AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"placeholder": "voce@email.com", "autofocus": True}),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "••••••••"}),
    )
    lembrar = forms.BooleanField(label="Lembrar de mim", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aplicar_classes()


class UsuarioCadastroForm(FormControlMixin, UserCreationForm):
    tipo_usuario = forms.ChoiceField(
        label="Quero usar a PontoCar para",
        choices=(
            (Usuario.TipoUsuario.COMPRADOR, "Comprar"),
            (Usuario.TipoUsuario.VENDEDOR, "Vender"),
            (Usuario.TipoUsuario.EMPRESA, "Sou empresa"),
        ),
        widget=forms.RadioSelect,
    )
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Sobrenome", max_length=150)
    cpf = forms.CharField(label="CPF", max_length=14, required=False)
    telefone = forms.CharField(label="Telefone / WhatsApp", max_length=20, required=False)
    email = forms.EmailField(label="E-mail")
    termos = forms.BooleanField(
        label="Li e aceito os termos de uso e a política de privacidade",
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = (
            "tipo_usuario",
            "first_name",
            "last_name",
            "cpf",
            "telefone",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirmar senha"
        self.fields["password1"].widget.attrs["placeholder"] = "Mínimo 8 caracteres"
        self.fields["password2"].widget.attrs["placeholder"] = "Repita a senha"
        self.aplicar_classes()

    def clean_cpf(self):
        cpf = "".join(ch for ch in self.cleaned_data.get("cpf", "") if ch.isdigit())
        if cpf and len(cpf) != 11:
            raise forms.ValidationError("Informe um CPF com 11 dígitos.")
        return cpf or None

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if Usuario.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta cadastrada com este e-mail.")
        return email


class UsuarioPerfilForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("first_name", "last_name", "telefone", "email")
        labels = {
            "first_name": "Nome",
            "last_name": "Sobrenome",
            "telefone": "Telefone / WhatsApp",
            "email": "E-mail",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aplicar_classes()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = Usuario.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este e-mail já está em uso.")
        return email


class AlterarSenhaForm(FormControlMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "Senha atual"
        self.fields["new_password1"].label = "Nova senha"
        self.fields["new_password2"].label = "Confirmar nova senha"
        for field in self.fields.values():
            field.widget.attrs["placeholder"] = "••••••••"
        self.aplicar_classes()
