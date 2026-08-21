from django.contrib import admin
from .models import Favorito

@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'veiculo', 'data_criacao')
    search_fields = ('usuario__email', 'veiculo__placa')
