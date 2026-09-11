from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views
from .password_reset import DefinirNovaSenhaForm, PasswordResetSeguroView

app_name = "usuarios"

urlpatterns = [
    path("entrar/", views.login_view, name="login"),
    path("sair/", views.logout_view, name="logout"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path(
        "recuperar-senha/",
        PasswordResetSeguroView.as_view(),
        name="password_reset",
    ),
    path(
        "recuperar-senha/enviado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="usuarios/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "redefinir-senha/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="usuarios/password_reset_confirm.html",
            form_class=DefinirNovaSenhaForm,
            success_url=reverse_lazy("usuarios:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "redefinir-senha/concluido/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="usuarios/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("painel/", views.painel, name="painel"),
    path("perfil/", views.perfil, name="perfil"),
    path("alterar-senha/", views.alterar_senha, name="alterar_senha"),
    path("gestao/usuarios/", views.admin_usuarios, name="admin_usuarios"),
]
