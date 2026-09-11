from pathlib import Path

from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError


EXTENSOES_IMAGEM = {
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".png": "PNG",
    ".webp": "WEBP",
}
EXTENSOES_DOCUMENTO = {".pdf", ".jpg", ".jpeg", ".png"}
MAX_PIXELS_IMAGEM = 40_000_000


def _reposicionar(arquivo):
    try:
        arquivo.seek(0)
    except (AttributeError, OSError):
        pass


def validar_imagem_upload(
    arquivo,
    *,
    limite_bytes,
    descricao="imagem",
    extensoes_permitidas=None,
    max_pixels=MAX_PIXELS_IMAGEM,
):
    """Valida tamanho, extensão, formato real e resolução de uma imagem."""
    if not arquivo:
        return arquivo

    if getattr(arquivo, "size", 0) > limite_bytes:
        limite_mb = limite_bytes // (1024 * 1024)
        raise ValidationError(f"A {descricao} deve ter no máximo {limite_mb} MB.")

    extensoes = extensoes_permitidas or set(EXTENSOES_IMAGEM)
    extensao = Path(getattr(arquivo, "name", "")).suffix.lower()
    if extensao not in extensoes:
        raise ValidationError(
            f"A {descricao} deve estar em formato JPG, PNG ou WEBP."
        )

    formato_esperado = EXTENSOES_IMAGEM.get(extensao)

    try:
        _reposicionar(arquivo)
        with Image.open(arquivo) as imagem:
            formato_real = (imagem.format or "").upper()
            largura, altura = imagem.size

            if largura <= 0 or altura <= 0:
                raise ValidationError(f"A {descricao} possui dimensões inválidas.")

            if largura * altura > max_pixels:
                raise ValidationError(
                    f"A {descricao} possui resolução excessivamente alta."
                )

            imagem.verify()
    except ValidationError:
        raise
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
        raise ValidationError(
            f"O arquivo enviado como {descricao} não é uma imagem válida."
        ) from exc
    finally:
        _reposicionar(arquivo)

    if formato_real not in set(EXTENSOES_IMAGEM.values()):
        raise ValidationError(f"O formato real da {descricao} não é permitido.")

    if formato_esperado != formato_real:
        raise ValidationError(
            f"A extensão do arquivo não corresponde ao conteúdo real da {descricao}."
        )

    return arquivo


def validar_documento_upload(arquivo, *, limite_bytes):
    """Aceita apenas PDF real ou imagens JPEG/PNG verificadas pelo conteúdo."""
    if not arquivo:
        return arquivo

    if getattr(arquivo, "size", 0) > limite_bytes:
        limite_mb = limite_bytes // (1024 * 1024)
        raise ValidationError(f"O arquivo deve ter no máximo {limite_mb} MB.")

    extensao = Path(getattr(arquivo, "name", "")).suffix.lower()
    if extensao not in EXTENSOES_DOCUMENTO:
        raise ValidationError("Envie um arquivo PDF, JPG ou PNG.")

    if extensao == ".pdf":
        try:
            _reposicionar(arquivo)
            conteudo = arquivo.read()
        finally:
            _reposicionar(arquivo)

        if not conteudo.startswith(b"%PDF-") or b"%%EOF" not in conteudo[-2048:]:
            raise ValidationError("O arquivo enviado não contém um PDF válido.")
        return arquivo

    return validar_imagem_upload(
        arquivo,
        limite_bytes=limite_bytes,
        descricao="imagem do documento",
        extensoes_permitidas={".jpg", ".jpeg", ".png"},
    )
