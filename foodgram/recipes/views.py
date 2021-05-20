from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.db.models import Sum
from django.db import transaction
from django.forms import ValidationError
from django.views.decorators.csrf import csrf_protect
from . import models, forms

User = get_user_model()


def index(request):
    tags = {'brekfast': True, 'lanch': True, 'dinner': True}
    user_id = request.user.id
    recipes = models.Recipe.objects.select_related(
        'author', 'ingredient').annotate(
        is_favorite=Exists(
            models.FavorRecipe.objects.filter(
                user_id=user_id,
                recipe_id=OuterRef('pk'),
            ),
        ),
        is_purchas=Exists(
            models.Purchas.objects.filter(
                user_id=user_id,
                recipe_id=OuterRef('pk'),
            ),
        ))
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {"page": page, 'recipes': recipes, 'index': True, 'tags': tags}
    )


def index_add_tag(request, tag):
    tags = {'brekfast': False, 'lanch': False, 'dinner': False}
    if tag == 'brekfast':
        recipes = models.Recipe.objects.filter(tag_brekfast=True)
        tags['brekfast'] = True
    elif tag == 'lanch':
        recipes = models.Recipe.objects.filter(tag_lanch=True)
        tags['lanch'] = True
    elif tag == 'dinner':
        recipes = models.Recipe.objects.filter(tag_dinner=True)
        tags['dinner'] = True
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {"page": page, 'recipes': recipes, 'index': True, 'tags': tags}
    )


def index_del_tag(request, tag):
    tags = {'brekfast': False, 'lanch': False, 'dinner': False}
    if tag == 'brekfast':
        recipes = models.Recipe.objects.exclude(tag_brekfast=True)
        tags['brekfast'] = False
    elif tag == 'lanch':
        recipes = models.Recipe.objects.exclude(tag_lanch=True)
        tags['lanch'] = False
    elif tag == 'dinner':
        recipes = models.Recipe.objects.exclude(tag_dinner=True)
        tags['dinner'] = False
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {"page": page, 'recipes': recipes, 'index': True, 'tags': tags}
    )


def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(models.Recipe, id=recipe_id)
    if request.user.favor_recipe.filter(recipe=recipe).exists():
        favor = True
    else:
        favor = False
    if request.user.shop_recipe.filter(recipe=recipe).exists():
        purchas = True
    else:
        purchas = False
    if request.user.follower.filter(idol=recipe.author).exists():
        follow = True
    else:
        follow = False
    ingredients = {
        ingredient: models.IngredientRecipe.objects.get(
            recipe=recipe,
            ingredient=ingredient
        ).quantity for ingredient in recipe.ingredient.all()}
    return render(
        request,
        'recipeDetail.html',
        {
            'recipe': recipe, 'ingredients': ingredients,
            'favor': favor, 'purchas': purchas, 'follow': follow
        }
    )


def author_page(request, author_id):
    user = request.user
    author = get_object_or_404(User, id=author_id)
    recipes = models.Recipe.objects.select_related(
        'author', 'ingredient').annotate(is_favorite=Exists(
            models.FavorRecipe.objects.filter(
                user_id=user.id,
                recipe_id=OuterRef('pk'),
            ),
        ),
        is_purchas=Exists(
            models.Purchas.objects.filter(
                user_id=user.id,
                recipe_id=OuterRef('pk'),
            ),
        )).filter(author_id=author_id)
    followers = [follower.user for follower in author.mentor.all()]
    if user in followers:
        follow = True
    else:
        follow = False
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "authorPage.html",
        {"page": page, 'author': author, 'follow': follow}
    )


def follow_list(request):
    user = request.user
    latest = models.User.objects.select_related('recipe').filter(
        mentor__user=user).annotate(
        is_follow=Exists(
            models.Follow.objects.filter(
                user_id=user.id,
                idol_id=OuterRef('pk'),
            ),
        ))
    paginator = Paginator(latest, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "follow.html",
        {"page": page, "paginator": paginator, 'follow_list': True}
    )


@login_required
def profile_follow(request, username):
    """starts following the author if it is not the user himself"""
    user = request.user
    author = User.objects.get(username=username)
    if author != user:
        follow = models.Follow.objects.get_or_create(author=author, user=user)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    """stops following the author"""
    user = request.user
    follow = models.Follow.objects.filter(author__username=username, user=user)
    follow.delete()
    return redirect('profile', username=username)


def get_ingredients(request):
    ingredients = {}
    for key, value in request.POST.items():
        # ingredients[value] = key
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[value] = request.POST[f'valueIngredient_{num}']
    return ingredients


@login_required
@csrf_protect
def new_recipe(request):
    """Creating a new recipe by an authorized user"""
    ingredients = get_ingredients(request)
    form = forms.RecipeForm(
        request.POST or None,
        files=request.FILES or None
    )
    if not form.is_valid():
        # raise ValidationError(form.errors)
        return render(
            request,
            'new_recipe.html',
            {'form': form, 'edit': False, 'new': True}
        )
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    models.IngredientRecipe.objects.filter(recipe=recipe).delete()
    objs = []
    for name, quantity in ingredients.items():
        ingredient = get_object_or_404(models.Ingredient, name=name)
        objs.append(models.IngredientRecipe(
            recipe=recipe,
            ingredient=ingredient,
            quantity=quantity
        )
        )
        models.IngredientRecipe.objects.bulk_create(objs)
        form.save_m2m
        return redirect('index')


@login_required
@csrf_protect
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(models.Recipe, id=recipe_id)
    ingredients = get_ingredients(request)
    form = forms.RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if not form.is_valid():
        return render(
            request,
            'new_recipe.html',
            {'form': form, 'edit': False, 'new': True}
        )
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    models.IngredientRecipe.objects.filter(recipe=recipe).delete()
    objs = []
    for name, quantity in ingredients.items():
        ingredient = get_object_or_404(models.Ingredient, name=name)
        objs.append(models.IngredientRecipe(
            recipe=recipe,
            ingredient=ingredient,
            quantity=quantity
        )
        )
        models.IngredientRecipe.objects.bulk_create(objs)
        form.save_m2m
        return redirect('index')


@login_required
def favor_recipes(request):
    user = request.user
    latest = models.Recipe.objects.annotate(
        is_favorite=Exists(
            models.FavorRecipe.objects.filter(
                user_id=user.id,
                recipe_id=OuterRef('pk'),
            )),
        is_purchas=Exists(
            models.Purchas.objects.filter(
                user_id=user.id,
                recipe_id=OuterRef('pk'),
            ),
        )).filter(favor_recipe__user=user)
    paginator = Paginator(latest, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "favor_recipes.html",
        {"page": page, "paginator": paginator, 'favor': True}
    )


@login_required
def shop_recipes(request):
    user = request.user
    recipes = models.Recipe.objects.filter(shop_recipe__user=user)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "shopList.html",
        {"page": page, "paginator": paginator, 'shop': True}
    )


def download_shoplist(request):
    filename = "shoplist.txt"
    recipes = models.Recipe.objects.filter(shop_recipe__user=request.user)
    ingredients = models.IngredientRecipe.objects.filter(
        recipe__in=recipes
    ).values('ingredient__name', 'ingredient__dimension'
             ).annotate(ingredient_quantity=Sum('quantity'))
    content = [f'{ingredient["ingredient__name"]} {ingredient["ingredient_quantity"]} {ingredient["ingredient__dimension"]} \n' for ingredient in ingredients]
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(
        filename)
    return response


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)
