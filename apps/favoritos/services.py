from django.core.exceptions import ValidationError
from django.db import transaction

from apps.veiculos.models import Veiculo

from .models import Favorito


STATUS_FAVORITAVEIS = {
    Veiculo.StatusVeiculo.DISPONIVEL,
    Veiculo.StatusVeiculo.RESERVADO,
}


@transaction.atomic
def alternar_favorito(*, usuario, veiculo):
    """Alterna um favorito aplicando as regras de acesso do catálogo público."""
    if veiculo.status not in STATUS_FAVORITAVEIS:
        raise ValidationError("Este anúncio não está disponível para ser favoritado.")

    if veiculo.proprietario_atual_id == usuario.id:
        raise ValidationError("Você não pode favoritar o seu próprio anúncio.")

    favorito, criado = Favorito.objects.get_or_create(usuario=usuario, veiculo=veiculo)
    if criado:
        return True
    favorito.delete()
    return False
