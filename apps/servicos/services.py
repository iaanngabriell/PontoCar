from django.db import transaction


@transaction.atomic
def salvar_servico(*, empresa, form):
    """Cria ou atualiza um serviço garantindo o vínculo com a empresa atual."""
    servico = form.save(commit=False)
    servico.empresa = empresa
    servico.save()
    return servico


@transaction.atomic
def excluir_servico(*, servico):
    servico.delete()
