from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from apps.core.rate_limit import (
    consumir_limite,
    obter_ip_cliente,
    resposta_limite_excedido,
)
from apps.empresas.models import Empresa, VerificacaoEmpresa
from apps.favoritos.models import Favorito
from apps.leads.services import registrar_interesse

from . import services
from .forms import LeadInteresseForm, VeiculoForm
from .models import MarcaVeiculo, ModeloVeiculo, Veiculo


PUBLIC_STATUSES = (
    Veiculo.StatusVeiculo.DISPONIVEL,
    Veiculo.StatusVeiculo.RESERVADO,
)

INTERESSE_LIMITE = 5
INTERESSE_JANELA_SEGUNDOS = 10 * 60


def _foto_exibicao(veiculo):
    fotos = list(veiculo.fotos.all())
    return next((foto for foto in fotos if foto.principal), fotos[0] if fotos else None)


def _empresa_do_anunciante(veiculo):
    if not veiculo.proprietario_atual_id:
        return None
    return (
        Empresa.objects.filter(representante=veiculo.proprietario_atual, ativa=True)
        .select_related("localizacao")
        .prefetch_related("verificacoes")
        .order_by("data_cadastro")
        .first()
    )


def _usuario_pode_vender(usuario):
    """
    Comprar e vender são capacidades da mesma conta.

    Qualquer usuário autenticado pode anunciar. A propriedade do veículo
    continua sendo validada individualmente nas views de edição/ação.
    """
    return usuario.is_authenticated


def _usuario_admin(usuario):
    return usuario.is_authenticated and (
        usuario.is_staff
        or usuario.is_superuser
        or usuario.tipo_usuario == "ADMINISTRADOR"
        or usuario.has_perm("veiculos.pode_moderar_veiculo")
    )


@require_GET
def catalogo_modelos_api(request):
    """Retorna somente modelos do catálogo local pertencentes à marca informada."""
    marca_id = request.GET.get("marca", "").strip()
    if not marca_id:
        return JsonResponse({"modelos": []})

    marca = get_object_or_404(MarcaVeiculo, pk=marca_id, ativa=True)
    modelos = list(
        ModeloVeiculo.objects.filter(marca=marca, ativo=True)
        .order_by("nome")
        .values("id", "nome")
    )
    return JsonResponse(
        {
            "marca": {"id": str(marca.id), "nome": marca.nome},
            "modelos": [{"id": str(item["id"]), "nome": item["nome"]} for item in modelos],
        }
    )


def catalogo(request):
    veiculos = (
        Veiculo.objects.filter(status__in=PUBLIC_STATUSES)
        .select_related("proprietario_atual", "marca_catalogo", "modelo_catalogo")
        .prefetch_related("fotos", "proprietario_atual__empresas__verificacoes")
    )

    marca = request.GET.get("marca", "").strip()
    modelo = request.GET.get("modelo", "").strip()
    ano_min = request.GET.get("ano_min", "").strip()
    ano_max = request.GET.get("ano_max", "").strip()
    preco_max = request.GET.get("preco_max", "").strip()
    cambio = request.GET.get("cambio", "").strip()
    combustivel = request.GET.get("combustivel", "").strip()
    vendedor = request.GET.get("vendedor", "").strip()
    ordem = request.GET.get("ordem", "recentes").strip()

    if marca:
        veiculos = veiculos.filter(marca__iexact=marca)
    if modelo:
        veiculos = veiculos.filter(modelo__icontains=modelo)
    if ano_min.isdigit():
        veiculos = veiculos.filter(ano_modelo__gte=int(ano_min))
    if ano_max.isdigit():
        veiculos = veiculos.filter(ano_modelo__lte=int(ano_max))
    if preco_max:
        try:
            veiculos = veiculos.filter(preco__lte=Decimal(preco_max.replace(",", ".")))
        except InvalidOperation:
            pass
    if cambio:
        veiculos = veiculos.filter(cambio=cambio)
    if combustivel:
        veiculos = veiculos.filter(combustivel=combustivel)
    if vendedor == "lojas":
        veiculos = veiculos.filter(
            proprietario_atual__empresas__ativa=True,
            proprietario_atual__empresas__verificacoes__status=VerificacaoEmpresa.Status.APROVADA,
        ).exclude(
            proprietario_atual__empresas__verificacoes__status=VerificacaoEmpresa.Status.SUSPENSA
        )
    elif vendedor == "particulares":
        veiculos = veiculos.exclude(proprietario_atual__empresas__ativa=True)

    ordenacoes = {
        "menor_preco": "preco",
        "maior_preco": "-preco",
        "recentes": "-data_cadastro",
        "menor_km": "quilometragem",
    }
    veiculos = veiculos.distinct().order_by(ordenacoes.get(ordem, "-data_cadastro"))

    paginator = Paginator(veiculos, 12)
    pagina = paginator.get_page(request.GET.get("pagina"))
    for veiculo in pagina.object_list:
        veiculo.foto_exibicao = _foto_exibicao(veiculo)
        veiculo.empresa_anunciante = _empresa_do_anunciante(veiculo)

    favoritos_ids = set()
    if request.user.is_authenticated:
        favoritos_ids = set(
            Favorito.objects.filter(usuario=request.user, veiculo__in=pagina.object_list)
            .values_list("veiculo_id", flat=True)
        )

    marcas = (
        Veiculo.objects.filter(status__in=PUBLIC_STATUSES)
        .exclude(marca="")
        .values_list("marca", flat=True)
        .distinct()
        .order_by("marca")
    )

    return render(
        request,
        "veiculos/catalogo.html",
        {
            "pagina": pagina,
            "total": paginator.count,
            "marcas": marcas,
            "cambios": Veiculo.CambioVeiculo.choices,
            "combustiveis": Veiculo.CombustivelVeiculo.choices,
            "favoritos_ids": favoritos_ids,
            "filtros": {
                "marca": marca,
                "modelo": modelo,
                "ano_min": ano_min,
                "ano_max": ano_max,
                "preco_max": preco_max,
                "cambio": cambio,
                "combustivel": combustivel,
                "vendedor": vendedor,
                "ordem": ordem,
            },
        },
    )


def detalhes(request, veiculo_id):
    veiculo = get_object_or_404(
        Veiculo.objects.select_related(
            "proprietario_atual", "marca_catalogo", "modelo_catalogo"
        ).prefetch_related("fotos"),
        id=veiculo_id,
        status__in=PUBLIC_STATUSES,
    )
    empresa = _empresa_do_anunciante(veiculo)
    fotos = list(veiculo.fotos.all())
    foto_principal = next((foto for foto in fotos if foto.principal), fotos[0] if fotos else None)

    eh_proprietario = bool(
        request.user.is_authenticated
        and veiculo.proprietario_atual_id == request.user.id
    )

    initial = {
        "mensagem": f"Olá! Tenho interesse neste {veiculo.marca} {veiculo.modelo} e gostaria de mais informações."
    }
    if request.user.is_authenticated:
        initial.update(
            {
                "nome": request.user.get_full_name(),
                "email": request.user.email,
                "telefone": request.user.telefone,
            }
        )

    form = None if eh_proprietario else LeadInteresseForm(request.POST or None, initial=initial)

    if request.method == "POST":
        if eh_proprietario:
            messages.error(request, "Você não pode enviar interesse para o seu próprio anúncio.")
            return redirect("veiculos:detalhes", veiculo_id=veiculo.id)

        if request.user.is_authenticated:
            identificador_interesse = f"user:{request.user.pk}"
        else:
            identificador_interesse = f"ip:{obter_ip_cliente(request)}"

        resultado = consumir_limite(
            chave=f"interesse:{identificador_interesse}",
            limite=INTERESSE_LIMITE,
            janela_segundos=INTERESSE_JANELA_SEGUNDOS,
        )
        if not resultado.permitido:
            return resposta_limite_excedido(
                request,
                resultado,
                "Muitos interesses enviados em pouco tempo. Aguarde e tente novamente.",
                titulo="Envio de interesse temporariamente bloqueado",
                voltar_url=request.path,
            )

        if form is not None and form.is_valid():
            try:
                registrar_interesse(
                    veiculo=veiculo,
                    comprador=request.user if request.user.is_authenticated else None,
                    dados=form.cleaned_data,
                )
            except ValidationError as exc:
                form.add_error(None, exc.messages[0] if exc.messages else "Não foi possível enviar o interesse.")
            else:
                messages.success(request, "Seu interesse foi enviado ao anunciante.")
                return redirect("veiculos:detalhes", veiculo_id=veiculo.id)

    semelhantes_qs = Veiculo.objects.filter(status__in=PUBLIC_STATUSES)
    if veiculo.marca_catalogo_id:
        semelhantes_qs = semelhantes_qs.filter(marca_catalogo_id=veiculo.marca_catalogo_id)
    else:
        semelhantes_qs = semelhantes_qs.filter(marca__iexact=veiculo.marca)

    semelhantes = list(
        semelhantes_qs.exclude(pk=veiculo.pk)
        .prefetch_related("fotos")
        .order_by("preco")[:3]
    )
    for item in semelhantes:
        item.foto_exibicao = _foto_exibicao(item)

    favorito = False
    if request.user.is_authenticated and not eh_proprietario:
        favorito = Favorito.objects.filter(usuario=request.user, veiculo=veiculo).exists()

    return render(
        request,
        "veiculos/detalhes.html",
        {
            "veiculo": veiculo,
            "empresa": empresa,
            "selo_ativo": bool(empresa and empresa.possui_selo_ativo()),
            "fotos": fotos,
            "foto_principal": foto_principal,
            "form": form,
            "semelhantes": semelhantes,
            "favorito": favorito,
            "eh_proprietario": eh_proprietario,
        },
    )


@login_required
@user_passes_test(_usuario_pode_vender)
def vendedor_veiculos(request):
    status = request.GET.get("status", "").strip()
    qs = Veiculo.objects.filter(proprietario_atual=request.user).prefetch_related("fotos").order_by("-data_cadastro")
    contagens = {valor: qs.filter(status=valor).count() for valor, _ in Veiculo.StatusVeiculo.choices}
    total = qs.count()
    if status:
        qs = qs.filter(status=status)
    veiculos = list(qs)
    for veiculo in veiculos:
        veiculo.foto_exibicao = _foto_exibicao(veiculo)
    return render(
        request,
        "veiculos/vendedor_lista.html",
        {
            "veiculos": veiculos,
            "status_atual": status,
            "status_choices": Veiculo.StatusVeiculo.choices,
            "contagens": contagens,
            "total": total,
        },
    )


@login_required
@user_passes_test(_usuario_pode_vender)
def vendedor_veiculo_novo(request):
    form = VeiculoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        rascunho = request.POST.get("acao") == "rascunho"
        try:
            veiculo = services.criar_veiculo_com_fotos(
                usuario=request.user,
                dados=form.cleaned_data,
                arquivos=request.FILES.getlist("fotos"),
                salvar_como_rascunho=rascunho,
            )
        except ValidationError as exc:
            form.add_error(None, exc.message)
        else:
            messages.success(
                request,
                "Anúncio salvo como rascunho." if rascunho else "Anúncio publicado com sucesso.",
            )
            return redirect("veiculos:vendedor_lista")
    return render(request, "veiculos/vendedor_form.html", {"form": form})


@login_required
@user_passes_test(_usuario_pode_vender)
def vendedor_veiculo_editar(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, proprietario_atual=request.user)
    form = VeiculoForm(request.POST or None, instance=veiculo)
    if request.method == "POST" and form.is_valid():
        try:
            services.atualizar_veiculo_com_fotos(
                veiculo=veiculo,
                dados=form.cleaned_data,
                arquivos=request.FILES.getlist("fotos"),
            )
        except ValidationError as exc:
            form.add_error(None, exc.message)
        else:
            messages.success(request, "Anúncio atualizado com sucesso.")
            return redirect("veiculos:vendedor_lista")
    return render(request, "veiculos/vendedor_form.html", {"form": form, "veiculo": veiculo})


@login_required
@user_passes_test(_usuario_pode_vender)
@require_POST
def vendedor_acao(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, proprietario_atual=request.user)
    acao = request.POST.get("acao")
    mapa = {
        "enviar_analise": services.enviar_para_analise,
        "reenviar_analise": services.reenviar_para_analise,
        "pausar": services.pausar_veiculo,
        "reativar": services.reativar_veiculo,
        "arquivar": services.arquivar_veiculo,
    }
    func = mapa.get(acao)
    if not func:
        messages.error(request, "Ação inválida.")
        return redirect("veiculos:vendedor_lista")
    try:
        func(veiculo=veiculo)
    except ValidationError as exc:
        messages.error(request, exc.message)
    else:
        messages.success(request, "Status do anúncio atualizado.")
    return redirect("veiculos:vendedor_lista")


@login_required
@user_passes_test(_usuario_admin)
def admin_moderacao(request):
    status = request.GET.get("status", Veiculo.StatusVeiculo.EM_ANALISE).strip()
    qs = (
        Veiculo.objects.select_related("proprietario_atual")
        .prefetch_related("fotos", "proprietario_atual__empresas")
        .order_by("-data_cadastro")
    )
    contagens = {valor: qs.filter(status=valor).count() for valor, _ in Veiculo.StatusVeiculo.choices}
    if status:
        qs = qs.filter(status=status)
    veiculos = list(qs)
    for veiculo in veiculos:
        veiculo.foto_exibicao = _foto_exibicao(veiculo)
        veiculo.empresa_anunciante = _empresa_do_anunciante(veiculo)
    return render(
        request,
        "veiculos/admin_moderacao.html",
        {
            "veiculos": veiculos,
            "status_atual": status,
            "status_choices": Veiculo.StatusVeiculo.choices,
            "contagens": contagens,
            "pode_moderar": request.user.has_perm("veiculos.pode_moderar_veiculo"),
        },
    )


@login_required
@user_passes_test(_usuario_admin)
@require_POST
def admin_moderacao_acao(request, veiculo_id):
    if not request.user.has_perm("veiculos.pode_moderar_veiculo"):
        messages.error(request, "Você não possui permissão para aprovar ou rejeitar anúncios.")
        return redirect("veiculos:admin_moderacao")

    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    acao = request.POST.get("acao")
    func = {
        "aprovar": services.aprovar_veiculo,
        "rejeitar": services.rejeitar_veiculo,
    }.get(acao)
    if not func:
        messages.error(request, "Ação de moderação inválida.")
        return redirect("veiculos:admin_moderacao")
    try:
        func(veiculo=veiculo)
    except ValidationError as exc:
        messages.error(request, exc.message)
    else:
        messages.success(request, "Anúncio atualizado com sucesso.")
    return redirect("veiculos:admin_moderacao")
