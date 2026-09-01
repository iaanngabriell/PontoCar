from django.urls import path

from . import views

app_name = "veiculos"

urlpatterns = [
    path("catalogo/", views.catalogo, name="catalogo"),
    path("veiculos/<uuid:veiculo_id>/", views.detalhes, name="detalhes"),
    path("vendedor/veiculos/", views.vendedor_veiculos, name="vendedor_lista"),
    path("vendedor/veiculos/novo/", views.vendedor_veiculo_novo, name="vendedor_novo"),
    path("vendedor/veiculos/<uuid:veiculo_id>/editar/", views.vendedor_veiculo_editar, name="vendedor_editar"),
    path("vendedor/veiculos/<uuid:veiculo_id>/acao/", views.vendedor_acao, name="vendedor_acao"),
    path("gestao/moderacao/", views.admin_moderacao, name="admin_moderacao"),
    path("gestao/moderacao/<uuid:veiculo_id>/acao/", views.admin_moderacao_acao, name="admin_moderacao_acao"),
]
