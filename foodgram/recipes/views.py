from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from . import models, forms

User = get_user_model()


def index(request):
    tags = {'breakfast': True, 'lanch': True, 'dinner': True}
    recipes = models.Recipe.objects.all()
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


def follow_list(request):
    user = request.user
    latest = models.User.objects.filter(mentor__user=user)
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


@login_required
def new_recipe(request):
    """Creating a new recipe by an authorized user"""
    form = forms.RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('index')
    return render(
        request,
        'new_recipe.html',
        {'form': form, 'edit': False, 'new': True}
        )


@login_required
def favor_recipes(request):
    user = request.user
    latest = models.Recipe.objects.filter(favor_recipe__user=user)
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
