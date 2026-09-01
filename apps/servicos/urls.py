from django.urls import path

from . import views

app_name = "servicos"

urlpatterns = [
    path("servicos/", views.lista, name="lista"),
    path("empresa/servicos/", views.empresa_servicos, name="empresa_lista"),
    path("empresa/servicos/novo/", views.empresa_servico_novo, name="empresa_novo"),
    path(
        "empresa/servicos/<uuid:servico_id>/editar/",
        views.empresa_servico_editar,
        name="empresa_editar",
    ),
    path(
        "empresa/servicos/<uuid:servico_id>/excluir/",
        views.empresa_servico_excluir,
        name="empresa_excluir",
    ),
]
