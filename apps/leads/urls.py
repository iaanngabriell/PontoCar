from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("vendedor/leads/", views.vendedor_leads, name="vendedor_leads"),
    path("vendedor/leads/<uuid:lead_id>/responder/", views.responder_lead, name="responder"),
    path(
        "minha-conta/interesses/<uuid:lead_id>/responder/",
        views.responder_interessado,
        name="responder_interessado",
    ),
]
