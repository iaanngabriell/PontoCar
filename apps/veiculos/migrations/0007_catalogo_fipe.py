import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("veiculos", "0006_criar_grupo_moderador"),
    ]

    operations = [
        migrations.CreateModel(
            name="MarcaVeiculo",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("codigo_externo", models.CharField(db_index=True, max_length=20, unique=True)),
                ("nome", models.CharField(db_index=True, max_length=80)),
                ("nome_origem", models.CharField(blank=True, max_length=100)),
                ("ativa", models.BooleanField(db_index=True, default=True)),
                ("sincronizado_em", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "marca de veículo",
                "verbose_name_plural": "marcas de veículos",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="ModeloVeiculo",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("codigo_externo", models.CharField(max_length=20)),
                ("nome", models.CharField(db_index=True, max_length=180)),
                ("ativo", models.BooleanField(db_index=True, default=True)),
                ("sincronizado_em", models.DateTimeField(auto_now=True)),
                (
                    "marca",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="modelos",
                        to="veiculos.marcaveiculo",
                    ),
                ),
            ],
            options={
                "verbose_name": "modelo de veículo",
                "verbose_name_plural": "modelos de veículos",
                "ordering": ["nome"],
            },
        ),
        migrations.AddConstraint(
            model_name="modeloveiculo",
            constraint=models.UniqueConstraint(
                fields=("marca", "codigo_externo"),
                name="uq_modelo_codigo_por_marca",
            ),
        ),
        migrations.AlterField(
            model_name="veiculo",
            name="marca",
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name="veiculo",
            name="modelo",
            field=models.CharField(max_length=180),
        ),
        migrations.AddField(
            model_name="veiculo",
            name="marca_catalogo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="veiculos_catalogo",
                to="veiculos.marcaveiculo",
            ),
        ),
        migrations.AddField(
            model_name="veiculo",
            name="modelo_catalogo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="veiculos_catalogo",
                to="veiculos.modeloveiculo",
            ),
        ),
    ]
