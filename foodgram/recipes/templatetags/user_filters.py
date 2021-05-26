from urllib.parse import urlencode

from django import template

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


@register.simple_tag
def tags_links(request, tag, all_tags):
    tags = request.GET.getlist('tags')
    if tags:
        new_request = request.GET.copy()
        if request.GET.getlist('page'):
            new_request.pop('page')
        if tag in tags:
            tags.remove(tag)
            new_request.setlist("tags", tags)
        else:
            new_request.appendlist("tags", tag)
        return new_request.urlencode()
    result = []
    for t in all_tags:
        if t != tag:
            result.append('tags=' + t)
    return '&'.join(result)


@register.simple_tag
def add_tags_to_pagination(request, param, value):
    new_request = request.GET.copy()
    new_request[param] = value

    return new_request.urlencode()


@register.filter
def is_selected(request, tag):
    tags = request.GET.getlist('tags')
    if tags:
        return tag in tags
    return True
