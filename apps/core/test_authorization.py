import json
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from apps.empresas.models import Empresa
from apps.favoritos.models import Favorito
from apps.leads.models import Lead
from apps.notificacoes.models import Notificacao
from apps.servicos.models import Servico
from apps.usuarios.models import Usuario
from apps.veiculos.models import Veiculo


class AuthorizationIDORTests(TestCase):
    def setUp(self):
        self.dono = Usuario.objects.create_user(
            username="dono-idor",
            email="dono-idor@pontocar.test",
            password="SenhaForte123!",
        )
        self.interessado = Usuario.objects.create_user(
            username="interessado-idor",
            email="interessado-idor@pontocar.test",
            password="SenhaForte123!",
        )
        self.terceiro = Usuario.objects.create_user(
            username="terceiro-idor",
            email="terceiro-idor@pontocar.test",
            password="SenhaForte123!",
        )

        self.veiculo = Veiculo.objects.create(
            proprietario_atual=self.dono,
            marca="Honda",
            modelo="Civic",
            ano_fabricacao=2020,
            ano_modelo=2020,
            preco=Decimal("120000.00"),
            quilometragem=50000,
            placa="IDA1B23",
            cor="Prata",
            status=Veiculo.StatusVeiculo.DISPONIVEL,
        )
        self.veiculo_privado = Veiculo.objects.create(
            proprietario_atual=self.dono,
            marca="Toyota",
            modelo="Corolla",
            ano_fabricacao=2021,
            ano_modelo=2021,
            preco=Decimal("130000.00"),
            quilometragem=40000,
            placa="IDB2C34",
            cor="Branco",
            status=Veiculo.StatusVeiculo.RASCUNHO,
        )

        self.lead = Lead.objects.create(
            veiculo=self.veiculo,
            comprador=self.interessado,
            anunciante=self.dono,
            nome="Interessado IDOR",
            email=self.interessado.email,
            telefone="63999999999",
            mensagem="Tenho interesse.",
        )

        self.notificacao = Notificacao.objects.create(
            usuario=self.dono,
            tipo=Notificacao.Tipo.NOVO_INTERESSE,
            titulo="Notificação privada",
            mensagem="Somente o destinatário pode abrir.",
            chave="idor:notificacao:dono",
            url=reverse("notificacoes:lista"),
        )

        self.empresa_dono = Empresa.objects.create(
            representante=self.dono,
            nome_fantasia="Oficina do Dono",
            razao_social="Oficina do Dono LTDA",
            cnpj="11111111000111",
            email="oficina-dono@pontocar.test",
            tipo_empresa=Empresa.TipoEmpresa.OFICINA,
        )
        self.empresa_terceiro = Empresa.objects.create(
            representante=self.terceiro,
            nome_fantasia="Oficina Terceira",
            razao_social="Oficina Terceira LTDA",
            cnpj="22222222000122",
            email="oficina-terceiro@pontocar.test",
            tipo_empresa=Empresa.TipoEmpresa.OFICINA,
        )
        self.servico = Servico.objects.create(
            empresa=self.empresa_dono,
            nome="Revisão",
            descricao="Revisão preventiva",
            preco=Decimal("350.00"),
            duracao_estimada=90,
        )

    def test_terceiro_nao_pode_editar_veiculo_de_outro_usuario(self):
        self.client.force_login(self.terceiro)
        resposta = self.client.get(
            reverse("veiculos:vendedor_editar", kwargs={"veiculo_id": self.veiculo.id})
        )
        self.assertEqual(resposta.status_code, 404)

    def test_terceiro_nao_pode_executar_acao_em_veiculo_de_outro_usuario(self):
        self.client.force_login(self.terceiro)
        resposta = self.client.post(
            reverse("veiculos:vendedor_acao", kwargs={"veiculo_id": self.veiculo.id}),
            {"acao": "pausar"},
        )
        self.assertEqual(resposta.status_code, 404)
        self.veiculo.refresh_from_db()
        self.assertEqual(self.veiculo.status, Veiculo.StatusVeiculo.DISPONIVEL)

    def test_terceiro_nao_pode_reordenar_fotos_de_veiculo_alheio(self):
        self.client.force_login(self.terceiro)
        resposta = self.client.post(
            reverse(
                "veiculos:vendedor_fotos_ordenar",
                kwargs={"veiculo_id": self.veiculo.id},
            ),
            data=json.dumps({"ordem": []}),
            content_type="application/json",
        )
        self.assertEqual(resposta.status_code, 404)

    def test_terceiro_nao_pode_responder_lead_como_anunciante(self):
        self.client.force_login(self.terceiro)
        resposta = self.client.post(
            reverse("leads:responder", kwargs={"lead_id": self.lead.id}),
            {"resposta": "Resposta indevida", "status": Lead.Status.CONTATADO},
        )
        self.assertEqual(resposta.status_code, 404)

    def test_terceiro_nao_pode_responder_lead_como_interessado(self):
        self.client.force_login(self.terceiro)
        resposta = self.client.post(
            reverse("leads:responder_interessado", kwargs={"lead_id": self.lead.id}),
            {"mensagem": "Mensagem indevida"},
        )
        self.assertEqual(resposta.status_code, 404)

    def test_terceiro_nao_pode_abrir_notificacao_de_outro_usuario(self):
        self.client.force_login(self.terceiro)
        resposta = self.client.post(
            reverse(
                "notificacoes:abrir",
                kwargs={"notificacao_id": self.notificacao.id},
            )
        )
        self.assertEqual(resposta.status_code, 404)
        self.notificacao.refresh_from_db()
        self.assertFalse(self.notificacao.lida)

    def test_terceiro_nao_pode_editar_servico_de_outra_empresa(self):
        self.client.force_login(self.terceiro)
        resposta = self.client.get(
            reverse("servicos:empresa_editar", kwargs={"servico_id": self.servico.id})
        )
        self.assertEqual(resposta.status_code, 404)

    def test_terceiro_nao_pode_excluir_servico_de_outra_empresa(self):
        self.client.force_login(self.terceiro)
        resposta = self.client.post(
            reverse("servicos:empresa_excluir", kwargs={"servico_id": self.servico.id})
        )
        self.assertEqual(resposta.status_code, 404)
        self.assertTrue(Servico.objects.filter(pk=self.servico.pk).exists())

    def test_nao_permite_favoritar_anuncio_privado_por_uuid(self):
        self.client.force_login(self.interessado)
        resposta = self.client.post(
            reverse("favoritos:alternar", kwargs={"veiculo_id": self.veiculo_privado.id})
        )
        self.assertEqual(resposta.status_code, 404)
        self.assertFalse(
            Favorito.objects.filter(
                usuario=self.interessado,
                veiculo=self.veiculo_privado,
            ).exists()
        )

    def test_proprietario_nao_pode_favoritar_proprio_anuncio(self):
        self.client.force_login(self.dono)
        resposta = self.client.post(
            reverse("favoritos:alternar", kwargs={"veiculo_id": self.veiculo.id})
        )
        self.assertEqual(resposta.status_code, 302)
        self.assertFalse(
            Favorito.objects.filter(usuario=self.dono, veiculo=self.veiculo).exists()
        )

    def test_favorito_de_anuncio_privado_nao_aparece_na_lista(self):
        Favorito.objects.create(usuario=self.interessado, veiculo=self.veiculo_privado)
        self.client.force_login(self.interessado)
        resposta = self.client.get(reverse("favoritos:interesses"))
        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn(
            self.veiculo_privado.id,
            [favorito.veiculo_id for favorito in resposta.context["favoritos"]],
        )

    def test_notificacao_nao_redireciona_para_host_externo(self):
        self.notificacao.url = "https://exemplo-malicioso.test/phishing"
        self.notificacao.save(update_fields=["url"])
        self.client.force_login(self.dono)
        resposta = self.client.post(
            reverse(
                "notificacoes:abrir",
                kwargs={"notificacao_id": self.notificacao.id},
            )
        )
        self.assertRedirects(
            resposta,
            reverse("notificacoes:lista"),
            fetch_redirect_response=False,
        )

    def test_next_externo_em_marcar_notificacoes_e_ignorado(self):
        self.client.force_login(self.dono)
        resposta = self.client.post(
            reverse("notificacoes:marcar_todas_lidas"),
            {"next": "https://exemplo-malicioso.test/phishing"},
        )
        self.assertRedirects(
            resposta,
            reverse("notificacoes:lista"),
            fetch_redirect_response=False,
        )

    def test_usuario_comum_nao_acessa_telas_administrativas(self):
        self.client.force_login(self.terceiro)
        for nome_url in (
            "usuarios:admin_usuarios",
            "veiculos:admin_moderacao",
            "vendas:admin_vendas",
        ):
            with self.subTest(url=nome_url):
                resposta = self.client.get(reverse(nome_url))
                self.assertNotEqual(resposta.status_code, 200)
