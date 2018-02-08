from django import template
import locale

locale.setlocale(locale.LC_ALL, '')
register = template.Library()


@register.filter()
def currency(value):
    return locale.currency(value, grouping=True)


@register.filter()
def addcss(field, css):
    return field.as_widget(attrs={"class": css})
