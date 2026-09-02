import re
from decimal import Decimal, InvalidOperation


_BR_THOUSANDS_RE = re.compile(r"^-?\d{1,3}(?:\.\d{3})+$")


def parse_decimal_br(value):
    """Converte valores monetários em formatos comuns pt-BR para Decimal.

    Exemplos aceitos: 128900, 128900.50, 128900,50, 128.900,50 e R$ 128.900,50.
    """
    if value is None or value == "":
        return None
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))

    text = str(value).strip()
    text = text.replace("R$", "").replace("\xa0", "").replace(" ", "")
    if not text:
        return None

    if "," in text:
        # No padrão brasileiro, ponto é separador de milhar e vírgula é decimal.
        text = text.replace(".", "").replace(",", ".")
    elif _BR_THOUSANDS_RE.fullmatch(text):
        # Ex.: 128.900 -> 128900
        text = text.replace(".", "")

    return Decimal(text)


def format_decimal_br(value, *, prefix=False, decimal_places=2):
    """Formata número usando ponto para milhar e vírgula para decimal."""
    try:
        number = parse_decimal_br(value)
    except (InvalidOperation, ValueError, TypeError):
        return ""

    if number is None:
        return ""

    places = max(0, int(decimal_places))
    formatted = f"{number:,.{places}f}"
    formatted = formatted.replace(",", "__MILHAR__").replace(".", ",").replace("__MILHAR__", ".")
    return f"R$ {formatted}" if prefix else formatted
