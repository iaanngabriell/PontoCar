from django.urls import path
from . import views

app_name = "leads"
urlpatterns = [path("vendedor/leads/", views.vendedor_leads, name="vendedor_leads")]
