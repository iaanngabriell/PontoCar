from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.leads.models import Lead
from apps.veiculos.models import HistoricoVeiculo, Veiculo

from .forms import EmpresaForm, LocalizacaoForm, VerificacaoEmpresaUploadForm
from .models import Empresa, Localizacao
from .services import enviar_documento_verificacao, salvar_empresa_com_localizacao


def empresas(request):
    categoria = request.GET.get("categoria", "").strip()
    qs = Empresa.objects.filter(ativa=True).select_related("localizacao")
    if categoria:
        qs = qs.filter(tipo_empresa=categoria)
    return render(
        request,
        "empresas/empresas.html",
        {
            "empresas": qs.order_by("nome_fantasia"),
            "categoria": categoria,
            "categorias": Empresa.TipoEmpresa.choices,
        },
    )


@login_required
def cadastro_empresa(request):
    empresa = Empresa.objects.filter(representante=request.user).order_by("data_cadastro").first()
    localizacao = None
    if empresa:
        localizacao = Localizacao.objects.filter(empresa=empresa).first()

    empresa_form = EmpresaForm(request.POST or None, instance=empresa, prefix="empresa")
    localizacao_form = LocalizacaoForm(
        request.POST or None,
        instance=localizacao,
        prefix="localizacao",
        initial={"cidade": "Palmas", "estado": "TO"} if not localizacao else None,
    )

    if request.method == "POST" and empresa_form.is_valid() and localizacao_form.is_valid():
        salvar_empresa_com_localizacao(
            usuario=request.user,
            empresa_form=empresa_form,
            localizacao_form=localizacao_form,
        )
        messages.success(request, "Dados da empresa salvos com sucesso.")
        return redirect("empresas:dashboard")

    return render(
        request,
        "empresas/empresa_cadastro.html",
        {"empresa_form": empresa_form, "localizacao_form": localizacao_form, "empresa": empresa},
    )


@login_required
def dashboard(request):
    empresa = Empresa.objects.filter(representante=request.user).order_by("data_cadastro").first()
    if not empresa:
        messages.info(request, "Cadastre os dados da sua empresa para acessar o painel.")
        return redirect("empresas:cadastro")

    veiculos = Veiculo.objects.filter(proprietario_atual=request.user)
    veiculos_ativos = veiculos.filter(
        status__in=[Veiculo.StatusVeiculo.DISPONIVEL, Veiculo.StatusVeiculo.RESERVADO]
    )
    leads = Lead.objects.filter(veiculo__proprietario_atual=request.user)
    vendas_pontocar = HistoricoVeiculo.objects.filter(
        dono_anterior=request.user,
        motivo=HistoricoVeiculo.MotivoEvento.VENDA_SITE,
    ).count()

    return render(
        request,
        "empresas/empresa_dashboard.html",
        {
            "empresa": empresa,
            "veiculos_ativos": veiculos_ativos.count(),
            "servicos_total": empresa.servicos.count(),
            "leads_total": leads.count(),
            "vendas_pontocar": vendas_pontocar,
            "veiculos_destaque": veiculos_ativos.prefetch_related("fotos").order_by("-data_cadastro")[:3],
            "selo_ativo": empresa.possui_selo_ativo(),
        },
    )


@login_required
def verificacao(request):
    empresa = (
        Empresa.objects.filter(representante=request.user)
        .prefetch_related("verificacoes")
        .order_by("data_cadastro")
        .first()
    )
    if not empresa:
        messages.info(request, "Cadastre sua empresa antes de enviar documentos para verificação.")
        return redirect("empresas:cadastro")

    form = VerificacaoEmpresaUploadForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        enviar_documento_verificacao(
            empresa=empresa,
            nome_documento=form.cleaned_data["nome_documento"],
            arquivo=form.cleaned_data["arquivo"],
            observacao=form.cleaned_data["observacao"],
        )
        messages.success(request, "Documento enviado para análise.")
        return redirect("empresas:verificacao")

    verificacoes = empresa.verificacoes.order_by("-data_envio")
    return render(
        request,
        "empresas/empresa_verificacao.html",
        {
            "empresa": empresa,
            "verificacoes": verificacoes,
            "form": form,
            "selo_ativo": empresa.possui_selo_ativo(),
        },
    )
