from django.db import transaction

from .models import Favorito


@transaction.atomic
def alternar_favorito(*, usuario, veiculo):
    favorito, criado = Favorito.objects.get_or_create(usuario=usuario, veiculo=veiculo)
    if criado:
        return True
    favorito.delete()
    return False
