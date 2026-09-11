from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("notificacoes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notificacao",
            name="tipo",
            field=models.CharField(
                choices=[
                    ("NOVO_INTERESSE", "Novo interesse"),
                    ("RESPOSTA_INTERESSE", "Resposta ao interesse"),
                    ("NOVA_PROPOSTA", "Nova proposta"),
                    ("PROPOSTA_ATUALIZADA", "Proposta atualizada"),
                ],
                max_length=30,
            ),
        ),
    ]
