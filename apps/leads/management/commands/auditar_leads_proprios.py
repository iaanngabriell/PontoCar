from django.core.management.base import BaseCommand
from django.db.models import F

from apps.leads.models import Lead


class Command(BaseCommand):
    help = "Identifica Leads legados enviados pelo proprietário ao próprio anúncio."

    def add_arguments(self, parser):
        parser.add_argument(
            "--remover",
            action="store_true",
            help="Remove os Leads inválidos encontrados. Sem esta opção, o comando apenas audita.",
        )

    def handle(self, *args, **options):
        invalidos = Lead.objects.filter(
            comprador_id=F("veiculo__proprietario_atual_id")
        ).select_related("comprador", "veiculo")

        total = invalidos.count()
        if not total:
            self.stdout.write(self.style.SUCCESS("Nenhum Lead próprio encontrado."))
            return

        self.stdout.write(self.style.WARNING(f"Foram encontrados {total} Lead(s) próprio(s):"))
        for lead in invalidos[:50]:
            self.stdout.write(
                f"  - {lead.id} | {lead.comprador.email if lead.comprador else 'sem conta'} | "
                f"{lead.veiculo.marca} {lead.veiculo.modelo} ({lead.veiculo.placa})"
            )

        if not options["remover"]:
            self.stdout.write(
                "Nenhum registro foi alterado. Para remover somente esses Leads inválidos, "
                "execute novamente com --remover."
            )
            return

        removidos, _ = invalidos.delete()
        self.stdout.write(self.style.SUCCESS(f"Limpeza concluída: {removidos} registro(s) removido(s)."))
