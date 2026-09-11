from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase
from PIL import Image

from .upload_validation import validar_documento_upload, validar_imagem_upload


class UploadValidationTests(SimpleTestCase):
    @staticmethod
    def _imagem(nome, formato):
        buffer = BytesIO()
        Image.new("RGB", (20, 20), "white").save(buffer, format=formato)
        return SimpleUploadedFile(nome, buffer.getvalue(), content_type="image/jpeg")

    def test_aceita_jpeg_real(self):
        arquivo = self._imagem("foto.jpg", "JPEG")
        self.assertIs(
            validar_imagem_upload(arquivo, limite_bytes=1024 * 1024),
            arquivo,
        )

    def test_rejeita_arquivo_falso_com_extensao_jpg(self):
        arquivo = SimpleUploadedFile(
            "foto.jpg",
            b"<script>alert('x')</script>",
            content_type="image/jpeg",
        )
        with self.assertRaises(ValidationError):
            validar_imagem_upload(arquivo, limite_bytes=1024 * 1024)

    def test_rejeita_extensao_diferente_do_formato_real(self):
        arquivo = self._imagem("foto.jpg", "PNG")
        with self.assertRaises(ValidationError):
            validar_imagem_upload(arquivo, limite_bytes=1024 * 1024)

    def test_rejeita_pdf_falso(self):
        arquivo = SimpleUploadedFile(
            "documento.pdf",
            b"isto nao e um pdf",
            content_type="application/pdf",
        )
        with self.assertRaises(ValidationError):
            validar_documento_upload(arquivo, limite_bytes=1024 * 1024)

    def test_aceita_pdf_com_assinatura_e_eof(self):
        arquivo = SimpleUploadedFile(
            "documento.pdf",
            b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\n%%EOF",
            content_type="application/pdf",
        )
        self.assertIs(
            validar_documento_upload(arquivo, limite_bytes=1024 * 1024),
            arquivo,
        )
