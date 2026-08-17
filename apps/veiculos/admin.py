from django.contrib import admin
from .models import Veiculo, HistoricoVeiculo

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    # Trocámos 'vendedor' por 'proprietario_atual' e adicionei a 'placa' para ficar mais fácil de gerir
    list_display = ('placa', 'marca', 'modelo', 'preco', 'status', 'proprietario_atual', 'quantidade_proprietarios')
    list_filter = ('status', 'marca')
    search_fields = ('marca', 'modelo', 'placa')

@admin.register(HistoricoVeiculo)
class HistoricoVeiculoAdmin(admin.ModelAdmin):
    # Nova tabela no painel para ver o ciclo de vida do carro
    list_display = ('veiculo', 'motivo', 'dono_anterior', 'novo_dono', 'data_evento')
    list_filter = ('motivo',)
    search_fields = ('veiculo__placa',)
