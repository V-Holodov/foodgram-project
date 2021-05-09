from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from . import models

User = get_user_model()


def index(request):
    recipes = models.Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page})


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(models.Recipe, id=recipe_id)
    ingredients = {
        ingredient: models.IngredientRecipe.objects.get(
            recipe=recipe,
            ingredient=ingredient
            ).quantity for ingredient in recipe.ingredient.all()}
    return render(
        request,
        'recipeDetail.html',
        {'recipe': recipe, 'ingredients': ingredients}
    )


def author_page(request, author_id):
    author = get_object_or_404(User, id=author_id)
    recipes = models.Recipe.objects.filter(author_id=author_id)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "authorPage.html", {"page": page, 'author': author})
