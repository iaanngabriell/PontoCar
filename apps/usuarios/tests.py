from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .models import Usuario


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class PasswordResetTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="recuperacao",
            email="recuperacao@pontocar.test",
            password="SenhaAntiga123!",
        )

    def test_tela_de_recuperacao_carrega(self):
        response = self.client.get(reverse("usuarios:password_reset"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Esqueci minha senha")

    def test_email_existente_envia_link_sem_expor_dados(self):
        response = self.client.post(
            reverse("usuarios:password_reset"),
            {"email": self.usuario.email},
        )
        self.assertRedirects(response, reverse("usuarios:password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Redefinição de senha", mail.outbox[0].subject)
        self.assertIn("/redefinir-senha/", mail.outbox[0].body)

    def test_email_inexistente_tem_mesma_resposta_sem_enumeracao(self):
        response = self.client.post(
            reverse("usuarios:password_reset"),
            {"email": "naoexiste@pontocar.test"},
        )
        self.assertRedirects(response, reverse("usuarios:password_reset_done"))
        self.assertEqual(len(mail.outbox), 0)

    def test_token_valido_permite_definir_nova_senha(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.usuario.pk))
        token = default_token_generator.make_token(self.usuario)
        url = reverse(
            "usuarios:password_reset_confirm",
            kwargs={"uidb64": uidb64, "token": token},
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(
            response.url,
            {
                "new_password1": "NovaSenhaForte456!",
                "new_password2": "NovaSenhaForte456!",
            },
        )
        self.assertRedirects(response, reverse("usuarios:password_reset_complete"))

        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.check_password("NovaSenhaForte456!"))

    def test_rate_limit_por_email_retorna_429(self):
        url = reverse("usuarios:password_reset")
        for _ in range(3):
            response = self.client.post(url, {"email": self.usuario.email})
            self.assertEqual(response.status_code, 302)

        response = self.client.post(url, {"email": self.usuario.email})
        self.assertEqual(response.status_code, 429)
        self.assertIn("Retry-After", response.headers)
