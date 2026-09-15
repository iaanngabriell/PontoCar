import json
import os
import re
import unicodedata
import urllib.error
import urllib.request

BASE_URL = "https://fipe.parallelum.com.br/api/v2"
TIMEOUT_SEGUNDOS = 25

# A FIPE usa alguns nomes históricos de marca. Na interface do PontoCar usamos
# a forma comercial mais reconhecível, sem perder o valor original no banco.
_ALIASES_MARCA = {
    "GM - CHEVROLET": "Chevrolet",
    "VW - VOLKSWAGEN": "Volkswagen",
}


class CatalogoFipeError(RuntimeError):
    pass


def normalizar_nome_marca(nome):
    nome = " ".join(str(nome or "").split()).strip()
    return _ALIASES_MARCA.get(nome.upper(), nome)


def chave_normalizada(valor):
    """Chave tolerante a caixa, acentos, hífens e espaços para reconciliação."""
    texto = unicodedata.normalize("NFKD", str(valor or ""))
    texto = "".join(ch for ch in texto if not unicodedata.combining(ch)).casefold()
    return re.sub(r"[^a-z0-9]+", "", texto)


def _headers():
    headers = {
        "Accept": "application/json",
        "User-Agent": "PontoCar/1.0 (+catalog-sync)",
    }
    token = os.environ.get("FIPE_API_TOKEN", "").strip()
    if token:
        headers["X-Subscription-Token"] = token
    return headers


def _get_json(caminho):
    url = f"{BASE_URL}/{caminho.lstrip('/')}"
    request = urllib.request.Request(url, headers=_headers(), method="GET")
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SEGUNDOS) as response:
            if response.status != 200:
                raise CatalogoFipeError(f"FIPE respondeu HTTP {response.status} em {url}.")
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise CatalogoFipeError(f"Não foi possível consultar o catálogo FIPE em {url}: {exc}") from exc


def listar_marcas_carros():
    dados = _get_json("cars/brands")
    if not isinstance(dados, list):
        raise CatalogoFipeError("Resposta inesperada ao listar marcas FIPE.")
    return dados


def listar_modelos_carros(codigo_marca):
    dados = _get_json(f"cars/brands/{codigo_marca}/models")
    if not isinstance(dados, list):
        raise CatalogoFipeError(f"Resposta inesperada ao listar modelos da marca {codigo_marca}.")
    return dados
