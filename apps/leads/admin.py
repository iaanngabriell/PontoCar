from django.contrib import admin

from .models import Lead, MensagemLead


class MensagemLeadInline(admin.TabularInline):
    model = MensagemLead
    extra = 0
    can_delete = False
    readonly_fields = ("autor", "tipo_autor", "texto", "criada_em")
    fields = readonly_fields

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("nome", "veiculo", "status", "comprador", "anunciante", "data_criacao")
    list_filter = ("status",)
    search_fields = ("nome", "email", "veiculo__placa")
    inlines = (MensagemLeadInline,)


@admin.register(MensagemLead)
class MensagemLeadAdmin(admin.ModelAdmin):
    list_display = ("lead", "tipo_autor", "autor", "criada_em")
    list_filter = ("tipo_autor", "criada_em")
    search_fields = ("texto", "lead__nome", "lead__email", "lead__veiculo__placa")
    readonly_fields = ("lead", "autor", "tipo_autor", "texto", "criada_em")

    def has_add_permission(self, request):
        return False
