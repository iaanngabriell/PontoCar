from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("", include("apps.usuarios.urls")),
    path("", include("apps.empresas.urls")),
    path("", include("apps.veiculos.urls")),
    path("", include("apps.servicos.urls")),
    path("", include("apps.leads.urls")),
    path("", include("apps.vendas.urls")),
    path("", include("apps.favoritos.urls")),
    path("", include("apps.seguros.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
