from django.core.exceptions import ValidationError
from django.db import transaction

from .models import FotoVeiculo


@transaction.atomic
def reordenar_fotos_veiculo(*, veiculo, foto_ids):
    """Reordena fotos do veículo e transforma a primeira em foto principal."""
    fotos = list(
        veiculo.fotos.select_for_update().order_by("ordem", "criado_em")
    )

    ids_atuais = [str(foto.id) for foto in fotos]
    ids_recebidos = [str(foto_id) for foto_id in foto_ids]

    if len(ids_recebidos) != len(ids_atuais):
        raise ValidationError("A lista de fotos enviada está incompleta.")

    if len(set(ids_recebidos)) != len(ids_recebidos):
        raise ValidationError("A ordem enviada contém fotos repetidas.")

    if set(ids_recebidos) != set(ids_atuais):
        raise ValidationError("A ordem enviada contém fotos que não pertencem ao veículo.")

    fotos_por_id = {str(foto.id): foto for foto in fotos}
    fotos_ordenadas = [fotos_por_id[foto_id] for foto_id in ids_recebidos]

    # Remove a foto principal atual antes de definir uma nova para respeitar
    # a constraint de uma única foto principal por veículo.
    veiculo.fotos.filter(principal=True).update(principal=False)

    for indice, foto in enumerate(fotos_ordenadas):
        foto.ordem = indice
        foto.principal = indice == 0

    if fotos_ordenadas:
        FotoVeiculo.objects.bulk_update(
            fotos_ordenadas,
            fields=["ordem", "principal"],
        )

    return fotos_ordenadas
