from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("sobre/", views.sobre, name="sobre"),
    path("termos-de-uso/", views.termos, name="termos"),
    path("politica-de-privacidade/", views.privacidade, name="privacidade"),
]
