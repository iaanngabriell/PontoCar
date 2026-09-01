from django.urls import path

from . import views

app_name = "favoritos"

urlpatterns = [
    path("comprador/interesses/", views.comprador_interesses, name="comprador_interesses"),
    path("favoritos/<uuid:veiculo_id>/alternar/", views.alternar, name="alternar"),
]
