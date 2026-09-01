import uuid
from pathlib import Path

from django.core.files.storage import default_storage
from django.db import transaction
from django.utils.text import get_valid_filename

from .models import Localizacao, VerificacaoEmpresa


@transaction.atomic
def salvar_empresa_com_localizacao(*, usuario, empresa_form, localizacao_form):
    """Cria/atualiza empresa e endereço principal na mesma transação."""
    empresa = empresa_form.save(commit=False)
    empresa.representante = usuario
    empresa.save()

    localizacao = localizacao_form.save(commit=False)
    localizacao.empresa = empresa
    localizacao.save()

    return empresa


@transaction.atomic
def enviar_documento_verificacao(*, empresa, nome_documento, arquivo, observacao=""):
    """Persiste o arquivo e cria um registro de verificação PENDENTE."""
    nome_original = get_valid_filename(Path(arquivo.name).name)
    caminho = f"empresas/documentos/{empresa.id}/{uuid.uuid4().hex}_{nome_original}"
    caminho_salvo = default_storage.save(caminho, arquivo)
    return VerificacaoEmpresa.objects.create(
        empresa=empresa,
        nome_documento=nome_documento,
        caminho_documento=caminho_salvo,
        observacao_solicitante=observacao,
        status=VerificacaoEmpresa.Status.PENDENTE,
    )
