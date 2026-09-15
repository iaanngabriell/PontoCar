from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .forms import VeiculoForm
from .models import MarcaVeiculo, ModeloVeiculo
from .services import _normalizar_dados_catalogo


class CatalogoVeiculosTests(TestCase):
    def setUp(self):
        self.toyota = MarcaVeiculo.objects.create(
            codigo_externo="56",
            nome="Toyota",
            nome_origem="Toyota",
        )
        self.volkswagen = MarcaVeiculo.objects.create(
            codigo_externo="59",
            nome="Volkswagen",
            nome_origem="VW - VolksWagen",
        )
        self.corolla = ModeloVeiculo.objects.create(
            marca=self.toyota,
            codigo_externo="1234",
            nome="Corolla XEi 2.0 Flex 16V Aut.",
        )
        self.golf = ModeloVeiculo.objects.create(
            marca=self.volkswagen,
            codigo_externo="5678",
            nome="Golf GTI 2.0 TSI 220cv Aut.",
        )

    def test_form_filtra_modelos_pela_marca_enviada(self):
        form = VeiculoForm(data={"marca_catalogo": str(self.toyota.id)})
        self.assertEqual(list(form.fields["modelo_catalogo"].queryset), [self.corolla])

    def test_form_rejeita_modelo_de_outra_marca(self):
        form = VeiculoForm(
            data={
                "marca_catalogo": str(self.toyota.id),
                "modelo_catalogo": str(self.golf.id),
                "versao": "",
                "ano_fabricacao": "2022",
                "ano_modelo": "2023",
                "quilometragem": "18000",
                "cambio": "AUTOMATICO",
                "combustivel": "FLEX",
                "cor": "Prata",
                "preco": "100.000,00",
                "placa": "ABC1D23",
                "descricao": "",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("modelo_catalogo", form.errors)

    def test_service_copia_nomes_canonicos_para_campos_legados(self):
        dados = _normalizar_dados_catalogo(
            {
                "marca_catalogo": self.toyota,
                "modelo_catalogo": self.corolla,
            }
        )
        self.assertEqual(dados["marca"], "Toyota")
        self.assertEqual(dados["modelo"], "Corolla XEi 2.0 Flex 16V Aut.")

    def test_service_rejeita_marca_modelo_incompativeis(self):
        with self.assertRaises(ValidationError):
            _normalizar_dados_catalogo(
                {
                    "marca_catalogo": self.toyota,
                    "modelo_catalogo": self.golf,
                }
            )

    def test_endpoint_retorna_somente_modelos_da_marca(self):
        response = self.client.get(
            reverse("veiculos:catalogo_modelos_api"),
            {"marca": str(self.toyota.id)},
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["marca"]["nome"], "Toyota")
        self.assertEqual(
            payload["modelos"],
            [{"id": str(self.corolla.id), "nome": self.corolla.nome}],
        )
