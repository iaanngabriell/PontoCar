from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Venda

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ('veiculo', 'comprador', 'valor_proposta', 'status', 'data_proposta')
    list_filter = ('status', 'data_proposta')
    search_fields = ('veiculo__placa', 'comprador__email')