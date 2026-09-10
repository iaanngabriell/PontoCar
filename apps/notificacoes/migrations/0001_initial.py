import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Notificacao",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("tipo", models.CharField(choices=[("NOVO_INTERESSE", "Novo interesse"), ("NOVA_PROPOSTA", "Nova proposta"), ("PROPOSTA_ATUALIZADA", "Proposta atualizada")], max_length=30)),
                ("titulo", models.CharField(max_length=140)),
                ("mensagem", models.CharField(max_length=280)),
                ("url", models.CharField(blank=True, default="", max_length=300)),
                ("chave", models.CharField(max_length=180, unique=True)),
                ("lida", models.BooleanField(default=False)),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                ("lida_em", models.DateTimeField(blank=True, null=True)),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="notificacoes", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ("-criada_em",),
            },
        ),
        migrations.AddIndex(
            model_name="notificacao",
            index=models.Index(fields=["usuario", "lida", "-criada_em"], name="notif_user_lida_idx"),
        ),
    ]
