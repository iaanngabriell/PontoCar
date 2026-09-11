from django.db import migrations


def criar_grupo_moderador(apps, schema_editor):
    """
    Cria (ou reutiliza) o grupo Moderador e a permissão customizada
    pode_moderar_veiculo.

    A permissão não pode ser obtida apenas com .get(), pois em um banco
    recém-criado (por exemplo, o banco temporário dos testes) as permissões
    customizadas normalmente só são criadas pelo Django no post_migrate.
    """
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")

    db_alias = schema_editor.connection.alias

    content_type, _ = ContentType.objects.using(db_alias).get_or_create(
        app_label="veiculos",
        model="veiculo",
    )

    permissao, _ = Permission.objects.using(db_alias).get_or_create(
        codename="pode_moderar_veiculo",
        content_type=content_type,
        defaults={
            "name": "Pode aprovar ou rejeitar anúncios de veículo",
        },
    )

    grupo, _ = Group.objects.using(db_alias).get_or_create(
        name="Moderador",
    )
    grupo.permissions.add(permissao)


def remover_grupo_moderador(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    db_alias = schema_editor.connection.alias
    Group.objects.using(db_alias).filter(name="Moderador").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("veiculos", "0005_migrar_status_pendente"),
        ("contenttypes", "0002_remove_content_type_name"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.RunPython(
            criar_grupo_moderador,
            remover_grupo_moderador,
        ),
    ]
