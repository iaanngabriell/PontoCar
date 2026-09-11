from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "cpf",
        "telefone",
        "tipo_usuario",
        "is_staff",
    )
    list_filter = ("tipo_usuario", "is_staff", "is_superuser", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Informações adicionais (PontoCar)",
            {
                "fields": (
                    "cpf",
                    "telefone",
                    "data_nascimento",
                    "foto_perfil",
                    "tipo_usuario",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Informações adicionais (PontoCar)",
            {
                "fields": (
                    "cpf",
                    "telefone",
                    "data_nascimento",
                    "foto_perfil",
                    "tipo_usuario",
                )
            },
        ),
    )
