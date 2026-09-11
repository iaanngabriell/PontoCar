from decimal import Decimal

from django.core.exceptions import PermissionDenied, ValidationError
from django.test import TestCase

from apps.notificacoes.models import Notificacao
from apps.usuarios.models import Usuario
from apps.veiculos.models import Veiculo

from .models import Lead, MensagemLead
from .services import registrar_interesse, responder_como_interessado, responder_interesse


class LeadServicesTests(TestCase):
    def setUp(self):
        self.dono = Usuario.objects.create_user(
            username="dono",
            email="dono@pontocar.test",
            password="SenhaForte123!",
        )
        self.interessado = Usuario.objects.create_user(
            username="interessado",
            email="interessado@pontocar.test",
            password="SenhaForte123!",
        )
        self.terceiro = Usuario.objects.create_user(
            username="terceiro",
            email="terceiro@pontocar.test",
            password="SenhaForte123!",
        )
        self.veiculo = Veiculo.objects.create(
            proprietario_atual=self.dono,
            marca="Volkswagen",
            modelo="Golf",
            ano_fabricacao=2017,
            ano_modelo=2017,
            preco=Decimal("128000.00"),
            quilometragem=95000,
            placa="ABC1D23",
            cor="Preto",
            status=Veiculo.StatusVeiculo.DISPONIVEL,
        )
        self.dados = {
            "nome": "Interessado Teste",
            "email": "interessado@pontocar.test",
            "telefone": "63999999999",
            "mensagem": "Tenho interesse no veículo.",
        }

    def _criar_lead(self):
        return registrar_interesse(
            veiculo=self.veiculo,
            comprador=self.interessado,
            dados=self.dados,
        )

    def test_nao_permite_interesse_no_proprio_anuncio(self):
        with self.assertRaises(ValidationError):
            registrar_interesse(
                veiculo=self.veiculo,
                comprador=self.dono,
                dados=self.dados,
            )
        self.assertEqual(Lead.objects.count(), 0)

    def test_interesse_cria_lead_mensagem_inicial_e_notifica_dono(self):
        lead = self._criar_lead()
        self.assertEqual(lead.anunciante, self.dono)
        self.assertEqual(lead.mensagens.count(), 1)
        primeira = lead.mensagens.get()
        self.assertEqual(primeira.tipo_autor, MensagemLead.TipoAutor.INTERESSADO)
        self.assertEqual(primeira.autor, self.interessado)
        self.assertTrue(
            Notificacao.objects.filter(
                usuario=self.dono,
                tipo=Notificacao.Tipo.NOVO_INTERESSE,
            ).exists()
        )

    def test_conversa_bidirecional_notifica_as_duas_pontas(self):
        lead = self._criar_lead()
        responder_interesse(
            lead=lead,
            anunciante=self.dono,
            resposta="Olá! Continua disponível.",
            status=Lead.Status.CONTATADO,
        )
        responder_como_interessado(
            lead=lead,
            interessado=self.interessado,
            texto="Ótimo. Posso visitar amanhã?",
        )

        mensagens = list(lead.mensagens.order_by("criada_em"))
        self.assertEqual(len(mensagens), 3)
        self.assertEqual(mensagens[1].tipo_autor, MensagemLead.TipoAutor.ANUNCIANTE)
        self.assertEqual(mensagens[2].tipo_autor, MensagemLead.TipoAutor.INTERESSADO)
        self.assertTrue(
            Notificacao.objects.filter(
                usuario=self.interessado,
                tipo=Notificacao.Tipo.RESPOSTA_INTERESSE,
            ).exists()
        )
        self.assertGreaterEqual(
            Notificacao.objects.filter(
                usuario=self.dono,
                tipo=Notificacao.Tipo.RESPOSTA_INTERESSE,
            ).count(),
            1,
        )

    def test_terceiro_nao_pode_responder_como_anunciante(self):
        lead = self._criar_lead()
        with self.assertRaises(PermissionDenied):
            responder_interesse(
                lead=lead,
                anunciante=self.terceiro,
                resposta="Resposta indevida",
                status=Lead.Status.CONTATADO,
            )

    def test_terceiro_nao_pode_responder_como_interessado(self):
        lead = self._criar_lead()
        with self.assertRaises(PermissionDenied):
            responder_como_interessado(
                lead=lead,
                interessado=self.terceiro,
                texto="Mensagem indevida",
            )
