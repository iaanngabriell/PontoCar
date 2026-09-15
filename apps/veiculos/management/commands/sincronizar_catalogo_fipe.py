from django.core.management.base import BaseCommand, CommandError

from apps.veiculos.catalogo_fipe import (
    CatalogoFipeError,
    chave_normalizada,
    listar_marcas_carros,
    listar_modelos_carros,
    normalizar_nome_marca,
)
from apps.veiculos.models import MarcaVeiculo, ModeloVeiculo, Veiculo


class Command(BaseCommand):
    help = (
        "Sincroniza marcas e modelos de carros da FIPE/Parallelum com o banco local "
        "e tenta reconciliar anúncios antigos sem alterar dados de forma ambígua."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--sem-reconciliar",
            action="store_true",
            help="Não tenta vincular anúncios antigos ao catálogo após a sincronização.",
        )

    def handle(self, *args, **options):
        try:
            marcas_api = listar_marcas_carros()
        except CatalogoFipeError as exc:
            raise CommandError(str(exc)) from exc

        codigos_marcas_ativas = []
        total_modelos = 0

        self.stdout.write(f"Sincronizando {len(marcas_api)} marcas FIPE...")

        for indice, item in enumerate(marcas_api, start=1):
            codigo = str(item.get("code", "")).strip()
            nome_origem = str(item.get("name", "")).strip()
            if not codigo or not nome_origem:
                self.stdout.write(self.style.WARNING(f"Marca ignorada por dados incompletos: {item!r}"))
                continue

            marca, _ = MarcaVeiculo.objects.update_or_create(
                codigo_externo=codigo,
                defaults={
                    "nome": normalizar_nome_marca(nome_origem),
                    "nome_origem": nome_origem,
                    "ativa": True,
                },
            )
            codigos_marcas_ativas.append(codigo)

            try:
                modelos_api = listar_modelos_carros(codigo)
            except CatalogoFipeError as exc:
                raise CommandError(
                    f"A marca {marca.nome} foi salva, mas a sincronização de modelos falhou: {exc}"
                ) from exc

            codigos_modelos_ativos = []
            for modelo_item in modelos_api:
                codigo_modelo = str(modelo_item.get("code", "")).strip()
                nome_modelo = " ".join(str(modelo_item.get("name", "")).split()).strip()
                if not codigo_modelo or not nome_modelo:
                    continue
                ModeloVeiculo.objects.update_or_create(
                    marca=marca,
                    codigo_externo=codigo_modelo,
                    defaults={"nome": nome_modelo, "ativo": True},
                )
                codigos_modelos_ativos.append(codigo_modelo)

            ModeloVeiculo.objects.filter(marca=marca).exclude(
                codigo_externo__in=codigos_modelos_ativos
            ).update(ativo=False)

            total_modelos += len(codigos_modelos_ativos)
            self.stdout.write(
                f"[{indice}/{len(marcas_api)}] {marca.nome}: {len(codigos_modelos_ativos)} modelos"
            )

        MarcaVeiculo.objects.exclude(codigo_externo__in=codigos_marcas_ativas).update(ativa=False)

        vinculados_marca = 0
        vinculados_modelo = 0
        if not options["sem_reconciliar"]:
            vinculados_marca, vinculados_modelo = self._reconciliar_existentes()

        self.stdout.write(
            self.style.SUCCESS(
                "Catálogo FIPE sincronizado: "
                f"{len(codigos_marcas_ativas)} marcas, {total_modelos} modelos. "
                f"Anúncios reconciliados: {vinculados_marca} marcas e {vinculados_modelo} modelos."
            )
        )

    def _reconciliar_existentes(self):
        marcas = list(MarcaVeiculo.objects.filter(ativa=True).prefetch_related("modelos"))
        mapa_marcas = {}
        for marca in marcas:
            chaves = {chave_normalizada(marca.nome), chave_normalizada(marca.nome_origem)}
            if " - " in marca.nome_origem:
                prefixo = marca.nome_origem.split(" - ", 1)[0].strip()
                if 1 < len(prefixo) <= 5:
                    chaves.add(chave_normalizada(prefixo))
            for chave in chaves:
                if chave:
                    mapa_marcas.setdefault(chave, marca)

        vinculados_marca = 0
        vinculados_modelo = 0

        for veiculo in Veiculo.objects.select_related("marca_catalogo", "modelo_catalogo").all():
            marca = veiculo.marca_catalogo
            update_fields = []

            if marca is None:
                marca = mapa_marcas.get(chave_normalizada(veiculo.marca))
                if marca is not None:
                    veiculo.marca_catalogo = marca
                    veiculo.marca = marca.nome
                    update_fields.extend(["marca_catalogo", "marca"])
                    vinculados_marca += 1
            elif veiculo.marca != marca.nome:
                veiculo.marca = marca.nome
                update_fields.append("marca")

            if marca is not None and veiculo.modelo_catalogo_id is None:
                mapa_modelos = {
                    chave_normalizada(modelo.nome): modelo
                    for modelo in marca.modelos.all()
                    if modelo.ativo
                }
                modelo = mapa_modelos.get(chave_normalizada(veiculo.modelo))
                if modelo is not None:
                    veiculo.modelo_catalogo = modelo
                    veiculo.modelo = modelo.nome
                    update_fields.extend(["modelo_catalogo", "modelo"])
                    vinculados_modelo += 1
            elif veiculo.modelo_catalogo_id and veiculo.modelo != veiculo.modelo_catalogo.nome:
                veiculo.modelo = veiculo.modelo_catalogo.nome
                update_fields.append("modelo")

            if update_fields:
                veiculo.save(update_fields=list(dict.fromkeys(update_fields)))

        return vinculados_marca, vinculados_modelo
