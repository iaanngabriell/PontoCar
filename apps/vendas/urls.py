from django.urls import path
from . import views

app_name = "vendas"
urlpatterns = [
    path("comprador/compras/", views.comprador_compras, name="comprador_compras"),
    path("gestao/vendas/", views.admin_vendas, name="admin_vendas"),
]
