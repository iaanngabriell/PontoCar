from django.core.management.base import BaseCommand, CommandError
from django.urls import NoReverseMatch, reverse

from apps.usuarios.forms import UsuarioCadastroForm
from apps.usuarios.models import Usuario


class Command(BaseCommand):
    help = "Audita a unificação de comprador e vendedor em conta pessoal."

    def handle(self, *args, **options):
        erros = []

        valores_validos = {
            Usuario.TipoUsuario.USUARIO,
            Usuario.TipoUsuario.EMPRESA,
            Usuario.TipoUsuario.ADMINISTRADOR,
        }

        legados = Usuario.objects.filter(
            tipo_usuario__in=("COMPRADOR", "VENDEDOR")
        ).count()
        invalidos = Usuario.objects.exclude(
            tipo_usuario__in=valores_validos
        ).count()

        totais = {
            valor: Usuario.objects.filter(tipo_usuario=valor).count()
            for valor in valores_validos
        }

        self.stdout.write("Auditoria de tipos de conta:")
        self.stdout.write(f"  Conta pessoal: {totais[Usuario.TipoUsuario.USUARIO]}")
        self.stdout.write(f"  Conta empresarial: {totais[Usuario.TipoUsuario.EMPRESA]}")
        self.stdout.write(
            f"  Administrador: {totais[Usuario.TipoUsuario.ADMINISTRADOR]}"
        )
        self.stdout.write(f"  Valores legados: {legados}")
        self.stdout.write(f"  Valores inválidos: {invalidos}")

        if legados:
            erros.append("ainda existem registros COMPRADOR/VENDEDOR no banco")
        if invalidos:
            erros.append("existem valores de tipo_usuario fora das opções válidas")

        escolhas_cadastro = {
            valor for valor, _rotulo in UsuarioCadastroForm().fields["tipo_usuario"].choices
        }
        escolhas_esperadas = {
            Usuario.TipoUsuario.USUARIO,
            Usuario.TipoUsuario.EMPRESA,
        }
        if escolhas_cadastro != escolhas_esperadas:
            erros.append("o cadastro público não está restrito a conta pessoal/empresarial")

        rotas = (
            "usuarios:painel",
            "favoritos:interesses",
            "vendas:compras",
            "seguros:minhas_cotacoes",
            "veiculos:vendedor_lista",
            "veiculos:vendedor_novo",
            "leads:vendedor_leads",
            "notificacoes:lista",
        )
        self.stdout.write("Auditoria de rotas:")
        for nome in rotas:
            try:
                url = reverse(nome)
            except NoReverseMatch:
                erros.append(f"rota não resolvida: {nome}")
                self.stdout.write(self.style.ERROR(f"  FALHA {nome}"))
            else:
                self.stdout.write(f"  OK {nome} -> {url}")

        if erros:
            for erro in erros:
                self.stderr.write(self.style.ERROR(f"- {erro}"))
            raise CommandError("A unificação apresentou inconsistências.")

        self.stdout.write(
            self.style.SUCCESS(
                "Unificação consistente: conta pessoal compra e vende sem tipos legados."
            )
        )
