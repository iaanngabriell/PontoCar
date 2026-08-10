from django.contrib import admin
from .models import Veiculo

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'ano_modelo', 'preco', 'status', 'vendedor')
    list_filter = ('status', 'marca', 'ano_modelo')
    search_fields = ('marca', 'modelo', 'placa')