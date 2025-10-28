from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply two numeric values."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''