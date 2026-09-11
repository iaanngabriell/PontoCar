from django.db import migrations, models


def unificar_contas_pessoais(apps, schema_editor):
    Usuario = apps.get_model("usuarios", "Usuario")
    Usuario.objects.filter(
        tipo_usuario__in=("COMPRADOR", "VENDEDOR")
    ).update(tipo_usuario="USUARIO")


def reverter_para_comprador(apps, schema_editor):
    """
    A reversão não consegue reconstruir se a conta era comprador ou vendedor.
    Para manter o banco válido no estado antigo, toda conta USUARIO volta como
    COMPRADOR. Nenhum relacionamento é apagado.
    """
    Usuario = apps.get_model("usuarios", "Usuario")
    Usuario.objects.filter(tipo_usuario="USUARIO").update(
        tipo_usuario="COMPRADOR"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("usuarios", "0003_usuario_foto_perfil"),
    ]

    operations = [
        migrations.RunPython(
            unificar_contas_pessoais,
            reverter_para_comprador,
        ),
        migrations.AlterField(
            model_name="usuario",
            name="tipo_usuario",
            field=models.CharField(
                choices=[
                    ("USUARIO", "Conta pessoal"),
                    ("EMPRESA", "Conta empresarial"),
                    ("ADMINISTRADOR", "Administrador"),
                ],
                default="USUARIO",
                max_length=20,
            ),
        ),
    ]
