from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Campos exibidos na listagem do Admin
    list_display = ('email', 'username', 'cpf', 'telefone', 'tipo_usuario', 'is_staff')
    
    # Filtros laterais
    list_filter = ('tipo_usuario', 'is_staff', 'is_superuser', 'is_active')
    
    # Organização dos campos ao editar/criar no Admin
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais (PontoCar)', {
            'fields': ('cpf', 'telefone', 'tipo_usuario')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais (PontoCar)', {
            'fields': ('cpf', 'telefone', 'tipo_usuario')
        }),
    )