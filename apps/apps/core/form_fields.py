from decimal import Decimal, InvalidOperation

from django import forms

from .formatters import format_decimal_br, parse_decimal_br


class MoedaBRField(forms.DecimalField):
    """DecimalField que aceita e reapresenta valores no padrão monetário pt-BR."""

    default_error_messages = {
        "invalid": "Informe um valor válido, por exemplo 128.900,00.",
    }

    def __init__(self, *args, **kwargs):
        attrs = {
            "inputmode": "decimal",
            "autocomplete": "off",
            "data-money": "brl",
        }
        widget = kwargs.pop("widget", None)
        if widget is None:
            widget = forms.TextInput(attrs=attrs)
        else:
            current = dict(widget.attrs)
            current.update(attrs)
            widget.attrs = current
        kwargs["widget"] = widget
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None
        try:
            parsed = parse_decimal_br(value)
        except (InvalidOperation, ValueError, TypeError):
            raise forms.ValidationError(self.error_messages["invalid"], code="invalid")
        return super().to_python(str(parsed))

    def prepare_value(self, value):
        if value in self.empty_values:
            return ""
        if isinstance(value, str):
            # Mantém o que o usuário digitou quando o form retorna com erro.
            return value
        if isinstance(value, (Decimal, int, float)):
            return format_decimal_br(value)
        return value
