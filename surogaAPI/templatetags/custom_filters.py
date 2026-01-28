from django import template

register = template.Library()

@register.filter
def decimal_to_hours(value):
    """
    Converte minutos para o formato de horas:minutos.
    """
    hours = value // 60
    minutes = value % 60
    return f"{hours:02d}:{minutes:02d}:00"
