from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("entrar/", views.login_view, name="login"),
    path("sair/", views.logout_view, name="logout"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("perfil/", views.perfil, name="perfil"),
    path("alterar-senha/", views.alterar_senha, name="alterar_senha"),
    path("gestao/usuarios/", views.admin_usuarios, name="admin_usuarios"),
]
