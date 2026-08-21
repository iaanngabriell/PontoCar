from django.db import migrations


def criar_grupo_moderador(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    grupo, _ = Group.objects.get_or_create(name='Moderador')

    permissao = Permission.objects.get(
        codename='pode_moderar_veiculo',
        content_type__app_label='veiculos',
    )
    grupo.permissions.add(permissao)


def remover_grupo_moderador(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Moderador').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('veiculos', '0005_migrar_status_pendente'),
    ]

    operations = [
        migrations.RunPython(criar_grupo_moderador, remover_grupo_moderador),
    ]