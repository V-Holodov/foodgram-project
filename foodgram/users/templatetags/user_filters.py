from django import template
from urllib.parse import urlencode

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


@register.filter
def changing_recipes(more_recipes):
    more_recipes -= 3
    if more_recipes in [11, 12, 13, 14]:
        varyrecipe = 'рецептов'
    elif more_recipes % 10 == 1:
        varyrecipe = 'рецепт'
    elif more_recipes % 10 in [2, 3, 4]:
        varyrecipe = 'рецепта'
    else:
        varyrecipe = 'рецептов'
    return varyrecipe
