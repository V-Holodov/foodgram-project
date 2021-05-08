from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from . import models


def index(request):
    recipes = models.Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page})


def recipe_detail(request, id):
    recipe = get_object_or_404(models.Recipe, id=id)
    ingredients = recipe.ingredient.all()
    return render(
        request,
        'recipeDetail.html',
        {'recipe': recipe, 'ingredients': ingredients}
    )
