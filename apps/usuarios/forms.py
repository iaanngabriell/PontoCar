from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm

from .models import Usuario


class FormControlMixin:
    def aplicar_classes(self):
        for field in self.fields.values():
            if isinstance(field.widget, forms.RadioSelect):
                continue
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-checkbox"
                continue
            field.widget.attrs["class"] = "form-control"


class LoginForm(FormControlMixin, AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "voce@email.com",
                "autofocus": True,
                "autocomplete": "email",
            }
        ),
    )
    password = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"placeholder": "••••••••", "autocomplete": "current-password"}
        ),
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
    first_name = forms.CharField(
        label="Nome",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Seu nome", "autocomplete": "given-name"}),
    )
    last_name = forms.CharField(
        label="Sobrenome",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Seu sobrenome", "autocomplete": "family-name"}),
    )
    cpf = forms.CharField(
        label="CPF",
        max_length=14,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "000.000.000-00",
                "inputmode": "numeric",
                "autocomplete": "off",
                "data-mask": "cpf",
            }
        ),
    )
    telefone = forms.CharField(
        label="Telefone / WhatsApp",
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "(63) 99999-9999",
                "inputmode": "tel",
                "autocomplete": "tel",
                "data-mask": "telefone",
            }
        ),
    )
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(attrs={"placeholder": "voce@email.com", "autocomplete": "email"}),
    )
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
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Mínimo 8 caracteres", "autocomplete": "new-password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Repita a senha", "autocomplete": "new-password"}
        )
        self.aplicar_classes()

    def clean_cpf(self):
        cpf = "".join(ch for ch in self.cleaned_data.get("cpf", "") if ch.isdigit())
        if cpf and len(cpf) != 11:
            raise forms.ValidationError("Informe um CPF com 11 dígitos.")
        if cpf and Usuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Já existe uma conta cadastrada com este CPF.")
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
