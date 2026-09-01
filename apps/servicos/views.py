from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.empresas.models import Empresa

from .forms import ServicoForm
from .models import Servico
from .services import excluir_servico, salvar_servico


def lista(request):
    busca = request.GET.get("q", "").strip()
    servicos = (
        Servico.objects.filter(empresa__ativa=True)
        .select_related("empresa", "empresa__localizacao")
        .order_by("nome")
    )

    if busca:
        servicos = servicos.filter(
            Q(nome__icontains=busca)
            | Q(descricao__icontains=busca)
            | Q(empresa__nome_fantasia__icontains=busca)
        )

    return render(
        request,
        "servicos/lista.html",
        {"servicos": servicos, "busca": busca},
    )


def _empresa_do_usuario(user):
    # Mantém a decisão atual do projeto: enquanto não houver seletor de empresa,
    # usa a primeira empresa vinculada ao representante.
    return (
        Empresa.objects.filter(representante=user)
        .order_by("data_cadastro")
        .first()
    )


def _obter_empresa_ou_redirecionar(request):
    empresa = _empresa_do_usuario(request.user)
    if empresa:
        return empresa, None

    messages.info(
        request,
        "Cadastre os dados da sua empresa antes de cadastrar serviços.",
    )
    return None, redirect("empresas:cadastro")


@login_required
def empresa_servicos(request):
    empresa, resposta = _obter_empresa_ou_redirecionar(request)
    if resposta:
        return resposta

    servicos = empresa.servicos.all().order_by("nome")
    return render(
        request,
        "servicos/empresa_servicos.html",
        {"empresa": empresa, "servicos": servicos},
    )


@login_required
def empresa_servico_novo(request):
    empresa, resposta = _obter_empresa_ou_redirecionar(request)
    if resposta:
        return resposta

    form = ServicoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        salvar_servico(empresa=empresa, form=form)
        messages.success(request, "Serviço cadastrado com sucesso.")
        return redirect("servicos:empresa_lista")

    return render(
        request,
        "servicos/servico_form.html",
        {"empresa": empresa, "form": form, "servico": None},
    )


@login_required
def empresa_servico_editar(request, servico_id):
    empresa, resposta = _obter_empresa_ou_redirecionar(request)
    if resposta:
        return resposta

    servico = get_object_or_404(Servico, pk=servico_id, empresa=empresa)
    form = ServicoForm(request.POST or None, instance=servico)

    if request.method == "POST" and form.is_valid():
        salvar_servico(empresa=empresa, form=form)
        messages.success(request, "Serviço atualizado com sucesso.")
        return redirect("servicos:empresa_lista")

    return render(
        request,
        "servicos/servico_form.html",
        {"empresa": empresa, "form": form, "servico": servico},
    )


@login_required
@require_POST
def empresa_servico_excluir(request, servico_id):
    empresa, resposta = _obter_empresa_ou_redirecionar(request)
    if resposta:
        return resposta

    servico = get_object_or_404(Servico, pk=servico_id, empresa=empresa)
    nome = servico.nome
    excluir_servico(servico=servico)
    messages.success(request, f'"{nome}" foi removido dos serviços da empresa.')
    return redirect("servicos:empresa_lista")
