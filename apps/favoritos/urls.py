from django.urls import path

from . import views

app_name = "favoritos"

urlpatterns = [
    # URL canônica da conta pessoal.
    path("minha-conta/interesses/", views.comprador_interesses, name="interesses"),

    # Compatibilidade com links/bookmarks anteriores à unificação.
    path("comprador/interesses/", views.comprador_interesses, name="comprador_interesses"),

    path("favoritos/<uuid:veiculo_id>/alternar/", views.alternar, name="alternar"),
]
