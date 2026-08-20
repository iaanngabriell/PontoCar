from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('nome', 'veiculo', 'status', 'comprador', 'data_criacao')
    list_filter = ('status',)
    search_fields = ('nome', 'email', 'veiculo__placa')
