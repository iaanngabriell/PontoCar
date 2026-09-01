from django.urls import path

from . import views

app_name = "seguros"

urlpatterns = [
    path("seguros/", views.lista, name="lista"),
    path("comprador/cotacoes/", views.comprador_cotacoes, name="comprador_cotacoes"),
]
