from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import AlterarSenhaForm, LoginForm, UsuarioCadastroForm, UsuarioPerfilForm
from .models import Usuario


def _eh_administrador(user):
    return user.is_authenticated and (
        user.is_staff
        or user.is_superuser
        or user.tipo_usuario == Usuario.TipoUsuario.ADMINISTRADOR
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")

    form = LoginForm(request=request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.get_user())
        if not form.cleaned_data.get("lembrar"):
            request.session.set_expiry(0)
        messages.success(request, "Login realizado com sucesso.")
        proxima_url = request.GET.get("next")
        if proxima_url and url_has_allowed_host_and_scheme(
            proxima_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(proxima_url)
        return redirect("core:index")

    return render(request, "usuarios/login.html", {"form": form})


@require_POST
def logout_view(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect("core:index")


def cadastro(request):
    if request.user.is_authenticated:
        return redirect("core:index")

    form = UsuarioCadastroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        auth_login(request, usuario)
        messages.success(request, "Conta criada com sucesso. Bem-vindo à PontoCar!")
        return redirect("core:index")

    return render(request, "usuarios/cadastro.html", {"form": form})


@login_required
def perfil(request):
    form = UsuarioPerfilForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Perfil atualizado com sucesso.")
        return redirect("usuarios:perfil")
    return render(request, "usuarios/perfil.html", {"form": form})


@login_required
def alterar_senha(request):
    form = AlterarSenhaForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        update_session_auth_hash(request, usuario)
        messages.success(request, "Senha alterada com sucesso.")
        return redirect("usuarios:perfil")
    return render(request, "usuarios/alterar_senha.html", {"form": form})


@user_passes_test(_eh_administrador)
def admin_usuarios(request):
    busca = request.GET.get("q", "").strip()
    usuarios = Usuario.objects.all().order_by("-date_joined")
    if busca:
        usuarios = usuarios.filter(
            Q(first_name__icontains=busca)
            | Q(last_name__icontains=busca)
            | Q(email__icontains=busca)
            | Q(cpf__icontains=busca)
        )
    return render(
        request,
        "usuarios/admin_usuarios.html",
        {"usuarios": usuarios, "busca": busca},
    )
