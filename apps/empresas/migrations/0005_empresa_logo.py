from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("empresas", "0004_verificacaoempresa"),
    ]

    operations = [
        migrations.AddField(
            model_name="empresa",
            name="logo",
            field=models.ImageField(blank=True, null=True, upload_to="empresas/logos/"),
        ),
    ]
