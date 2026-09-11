import uuid

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrar_historico_existente(apps, schema_editor):
    Lead = apps.get_model("leads", "Lead")
    MensagemLead = apps.get_model("leads", "MensagemLead")
    db_alias = schema_editor.connection.alias

    for lead in Lead.objects.using(db_alias).select_related("veiculo").iterator():
        anunciante_id = lead.veiculo.proprietario_atual_id
        if anunciante_id:
            Lead.objects.using(db_alias).filter(pk=lead.pk).update(anunciante_id=anunciante_id)

        texto_inicial = (lead.mensagem or "").strip()
        if texto_inicial:
            mensagem = MensagemLead.objects.using(db_alias).create(
                lead_id=lead.pk,
                autor_id=lead.comprador_id,
                tipo_autor="INTERESSADO",
                texto=texto_inicial[:1500],
            )
            MensagemLead.objects.using(db_alias).filter(pk=mensagem.pk).update(
                criada_em=lead.data_criacao
            )

        resposta = (lead.resposta_anunciante or "").strip()
        if resposta:
            mensagem = MensagemLead.objects.using(db_alias).create(
                lead_id=lead.pk,
                autor_id=anunciante_id,
                tipo_autor="ANUNCIANTE",
                texto=resposta[:1500],
            )
            if lead.data_resposta:
                MensagemLead.objects.using(db_alias).filter(pk=mensagem.pk).update(
                    criada_em=lead.data_resposta
                )


class Migration(migrations.Migration):
    dependencies = [
        ("leads", "0002_lead_resposta_anunciante"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="lead",
            name="anunciante",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="leads_recebidos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="MensagemLead",
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
                (
                    "tipo_autor",
                    models.CharField(
                        choices=[
                            ("INTERESSADO", "Interessado"),
                            ("ANUNCIANTE", "Anunciante"),
                        ],
                        max_length=20,
                    ),
                ),
                ("texto", models.TextField(max_length=1500)),
                ("criada_em", models.DateTimeField(auto_now_add=True)),
                (
                    "autor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="mensagens_lead",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "lead",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mensagens",
                        to="leads.lead",
                    ),
                ),
            ],
            options={"ordering": ("criada_em", "id")},
        ),
        migrations.RunPython(migrar_historico_existente, migrations.RunPython.noop),
    ]
