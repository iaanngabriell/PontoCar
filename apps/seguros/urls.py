from django.urls import path

from . import views

app_name = "seguros"

urlpatterns = [
    path("seguros/", views.lista, name="lista"),

    # URL canônica da conta pessoal.
    path("minha-conta/seguros/", views.comprador_cotacoes, name="minhas_cotacoes"),

    # Compatibilidade com links/bookmarks anteriores à unificação.
    path("comprador/cotacoes/", views.comprador_cotacoes, name="comprador_cotacoes"),
]
