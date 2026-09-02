from decimal import Decimal, InvalidOperation

from django import template

from apps.core.formatters import format_decimal_br, parse_decimal_br

register = template.Library()


@register.filter
def get_item(mapping, key):
    if not mapping:
        return 0
    return mapping.get(key, 0)


@register.filter
def brl(value):
    """Exibe um número como moeda brasileira: R$ 128.900,00."""
    formatted = format_decimal_br(value, prefix=True)
    return formatted or "—"


@register.filter
def numero_br(value, decimal_places=0):
    """Formata números com separador de milhar brasileiro."""
    try:
        number = parse_decimal_br(value)
        if number is None:
            return "—"
        places = int(decimal_places)
    except (InvalidOperation, ValueError, TypeError):
        return value
    return format_decimal_br(number, decimal_places=places)
