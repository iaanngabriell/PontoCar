from django.db import migrations


def migrar_pendente_para_reservado(apps, schema_editor):
    Veiculo = apps.get_model('veiculos', 'Veiculo')
    Veiculo.objects.filter(status='PENDENTE').update(status='RESERVADO')


def reverter(apps, schema_editor):
    Veiculo = apps.get_model('veiculos', 'Veiculo')
    Veiculo.objects.filter(status='RESERVADO').update(status='PENDENTE')


class Migration(migrations.Migration):

    dependencies = [
        ('veiculos', '0004_alter_veiculo_options_alter_veiculo_status'),
    ]

    operations = [
        migrations.RunPython(migrar_pendente_para_reservado, reverter),
    ]