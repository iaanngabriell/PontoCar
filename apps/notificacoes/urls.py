from django.urls import path

from . import views

app_name = "notificacoes"

urlpatterns = [
    path("notificacoes/", views.lista, name="lista"),
    path("notificacoes/<uuid:notificacao_id>/abrir/", views.abrir, name="abrir"),
    path("notificacoes/marcar-todas-lidas/", views.marcar_todas_lidas, name="marcar_todas_lidas"),
]
