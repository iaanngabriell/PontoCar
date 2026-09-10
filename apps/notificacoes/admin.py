from django.contrib import admin

from .models import Notificacao


@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "usuario", "tipo", "lida", "criada_em")
    list_filter = ("tipo", "lida", "criada_em")
    search_fields = ("titulo", "mensagem", "usuario__email")
    readonly_fields = ("criada_em", "lida_em", "chave")
