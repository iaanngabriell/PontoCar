from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("leads", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lead",
            name="resposta_anunciante",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="lead",
            name="data_resposta",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
