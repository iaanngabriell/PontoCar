from django.core.exceptions import ValidationError
from django.db import transaction

from .models import FotoVeiculo, Veiculo

LIMITE_FOTOS = 8
LIMITE_BYTES_POR_FOTO = 8 * 1024 * 1024


def _validar_fotos(arquivos, *, existentes=0):
    arquivos = list(arquivos)
    if existentes + len(arquivos) > LIMITE_FOTOS:
        raise ValidationError(f"Um veículo pode ter no máximo {LIMITE_FOTOS} fotos.")
    for arquivo in arquivos:
        if getattr(arquivo, "size", 0) > LIMITE_BYTES_POR_FOTO:
            raise ValidationError(f"A foto '{arquivo.name}' excede o limite de 8 MB.")
        content_type = getattr(arquivo, "content_type", "") or ""
        if content_type and not content_type.startswith("image/"):
            raise ValidationError(f"O arquivo '{arquivo.name}' não é uma imagem válida.")
    return arquivos


@transaction.atomic
def criar_veiculo_com_fotos(*, usuario, dados, arquivos=(), salvar_como_rascunho=False):
    """Cria o anúncio e suas fotos em uma única transação."""
    arquivos = _validar_fotos(arquivos)
    veiculo = Veiculo.objects.create(
        proprietario_atual=usuario,
        status=(
            Veiculo.StatusVeiculo.RASCUNHO
            if salvar_como_rascunho
            else Veiculo.StatusVeiculo.DISPONIVEL
        ),
        **dados,
    )
    adicionar_fotos(veiculo=veiculo, arquivos=arquivos)
    return veiculo


@transaction.atomic
def adicionar_fotos(*, veiculo, arquivos):
    """Adiciona fotos respeitando limite e uma única foto principal."""
    existentes = veiculo.fotos.count()
    arquivos = _validar_fotos(arquivos, existentes=existentes)
    possui_principal = veiculo.fotos.filter(principal=True).exists()

    for indice, arquivo in enumerate(arquivos, start=existentes):
        FotoVeiculo.objects.create(
            veiculo=veiculo,
            imagem=arquivo,
            principal=(not possui_principal and indice == existentes),
            ordem=indice,
            texto_alternativo=f"{veiculo.marca} {veiculo.modelo}",
        )
    return veiculo


@transaction.atomic
def atualizar_veiculo_com_fotos(*, veiculo, dados, arquivos=()):
    """Atualiza apenas dados editáveis do anúncio e opcionalmente acrescenta fotos."""
    arquivos = _validar_fotos(arquivos, existentes=veiculo.fotos.count())
    campos = []
    for campo, valor in dados.items():
        setattr(veiculo, campo, valor)
        campos.append(campo)
    if campos:
        veiculo.save(update_fields=campos)
    adicionar_fotos(veiculo=veiculo, arquivos=arquivos)
    return veiculo


@transaction.atomic
def enviar_para_analise(*, veiculo):
    """RASCUNHO -> EM_ANALISE. Vendedor pede a publicação do anúncio."""
    if veiculo.status != Veiculo.StatusVeiculo.RASCUNHO:
        raise ValidationError("Só é possível enviar para análise um anúncio em rascunho.")
    veiculo.status = Veiculo.StatusVeiculo.EM_ANALISE
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def aprovar_veiculo(*, veiculo):
    """EM_ANALISE -> DISPONIVEL. Ação de moderação."""
    if veiculo.status != Veiculo.StatusVeiculo.EM_ANALISE:
        raise ValidationError("Só é possível aprovar um anúncio em análise.")
    veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def rejeitar_veiculo(*, veiculo):
    """EM_ANALISE -> REJEITADO. Ação de moderação."""
    if veiculo.status != Veiculo.StatusVeiculo.EM_ANALISE:
        raise ValidationError("Só é possível rejeitar um anúncio em análise.")
    veiculo.status = Veiculo.StatusVeiculo.REJEITADO
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def reenviar_para_analise(*, veiculo):
    """REJEITADO -> EM_ANALISE."""
    if veiculo.status != Veiculo.StatusVeiculo.REJEITADO:
        raise ValidationError("Só é possível reenviar um anúncio rejeitado.")
    veiculo.status = Veiculo.StatusVeiculo.EM_ANALISE
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def reservar_veiculo(*, veiculo):
    """DISPONIVEL -> RESERVADO."""
    if veiculo.status != Veiculo.StatusVeiculo.DISPONIVEL:
        raise ValidationError("Só é possível reservar um veículo disponível.")
    veiculo.status = Veiculo.StatusVeiculo.RESERVADO
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def liberar_veiculo(*, veiculo):
    """RESERVADO -> DISPONIVEL."""
    if veiculo.status != Veiculo.StatusVeiculo.RESERVADO:
        raise ValidationError("Só é possível liberar um veículo reservado.")
    veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def marcar_vendido(*, veiculo):
    """DISPONIVEL ou RESERVADO -> VENDIDO."""
    if veiculo.status not in (
        Veiculo.StatusVeiculo.DISPONIVEL,
        Veiculo.StatusVeiculo.RESERVADO,
    ):
        raise ValidationError("Só é possível vender um veículo disponível ou reservado.")
    veiculo.status = Veiculo.StatusVeiculo.VENDIDO
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def reativar_veiculo(*, veiculo):
    """VENDIDO ou PAUSADO -> DISPONIVEL."""
    if veiculo.status not in (
        Veiculo.StatusVeiculo.VENDIDO,
        Veiculo.StatusVeiculo.PAUSADO,
    ):
        raise ValidationError("Só é possível reativar um veículo vendido ou pausado.")
    veiculo.status = Veiculo.StatusVeiculo.DISPONIVEL
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def pausar_veiculo(*, veiculo):
    """DISPONIVEL -> PAUSADO."""
    if veiculo.status != Veiculo.StatusVeiculo.DISPONIVEL:
        raise ValidationError("Só é possível pausar um veículo disponível.")
    veiculo.status = Veiculo.StatusVeiculo.PAUSADO
    veiculo.save(update_fields=["status"])
    return veiculo


@transaction.atomic
def arquivar_veiculo(*, veiculo):
    """PAUSADO -> ARQUIVADO."""
    if veiculo.status != Veiculo.StatusVeiculo.PAUSADO:
        raise ValidationError("Só é possível arquivar um veículo pausado.")
    veiculo.status = Veiculo.StatusVeiculo.ARQUIVADO
    veiculo.save(update_fields=["status"])
    return veiculo
