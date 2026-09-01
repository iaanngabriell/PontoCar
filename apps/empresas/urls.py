from django.urls import path

from . import views

app_name = "empresas"

urlpatterns = [
    path("empresas/", views.empresas, name="lista"),
    path("empresa/cadastro/", views.cadastro_empresa, name="cadastro"),
    path("empresa/dashboard/", views.dashboard, name="dashboard"),
    path("empresa/verificacao/", views.verificacao, name="verificacao"),
]
