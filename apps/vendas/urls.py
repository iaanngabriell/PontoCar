from django.urls import path

from . import views

app_name = "vendas"

urlpatterns = [
    # URL canônica da conta pessoal.
    path("minha-conta/compras/", views.comprador_compras, name="compras"),

    # Compatibilidade com links/bookmarks anteriores à unificação.
    path("comprador/compras/", views.comprador_compras, name="comprador_compras"),

    path("gestao/vendas/", views.admin_vendas, name="admin_vendas"),
]
