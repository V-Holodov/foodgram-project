import operator
from functools import reduce

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef, Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView

from . import forms, models

User = get_user_model()

PAGINATOR_SIZE = 6


class IsFavoriteMixin:
    """Add annotation with favorite mark to the View."""

    def get_queryset(self):
        qs = super().get_queryset()
        qs = (
            qs
            .select_related('author')
            .with_is_recipe(user_id=self.request.user.id)
        )
        return qs


def filter_qs_by_tags(request, queryset):
    tags = request.GET.getlist('tags')
    if tags:
        tag_dict = [Q(**{f'tag_{tag}': True}) for tag in tags]
        return queryset.filter(reduce(operator.or_, tag_dict))
    return queryset


class BaseRecipeListView(IsFavoriteMixin, ListView):
    """Base view for Recipe list."""
    context_object_name = 'recipes'
    queryset = models.Recipe.objects.all()
    paginate_by = PAGINATOR_SIZE
    page_title = None

    def get_context_data(self, **kwargs):
        kwargs.update({'page_title': self._get_page_title()})
        context = super().get_context_data(**kwargs)
        context['tags'] = ['breakfast', 'lunch', 'dinner']
        return context

    def _get_page_title(self):
        assert self.page_title, f"Attribute 'page_title' not set for {self.__class__.__name__}"  # noqa
        return self.page_title


class IndexView(BaseRecipeListView):
    """Main page that displays list of Recipes."""
    page_title = 'Рецепты'
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return filter_qs_by_tags(self.request, qs)


class FavoriteView(LoginRequiredMixin, BaseRecipeListView):
    """List of current user's favorite Recipes."""
    page_title = 'Избранное'
    template_name = 'favor_recipes.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(favor_recipe__user=self.request.user)
        return filter_qs_by_tags(self.request, qs)


class ProfileView(BaseRecipeListView):
    """User's page with its name and list of authored Recipes."""
    template_name = 'authorPage.html'

    def get(self, request, *args, **kwargs):
        self.author = get_object_or_404(User, id=kwargs.get('author_id'))
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.author)
        return filter_qs_by_tags(self.request, qs)

    def _get_page_title(self):
        return self.author.get_full_name()


def recipe_detail(request, recipe_id):
    """Page with Recipe details."""
    recipe = get_object_or_404(models.Recipe, id=recipe_id)
    favor = request.user.favor_recipe.filter(recipe=recipe).exists()
    purchas = request.user.shop_recipe.filter(recipe=recipe).exists()
    follow = request.user.follower.filter(idol=recipe.author).exists()
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


def follow_list(request):
    """Displaying a list of following authors."""
    user = request.user
    latest = models.User.objects.filter(
        mentor__user=user).annotate(
        is_follow=Exists(
            models.Follow.objects.filter(
                user_id=user.id,
                idol_id=OuterRef('pk'),
            ),
        ))
    paginator = Paginator(latest, PAGINATOR_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "follow.html",
        {"page": page, "paginator": paginator, 'follow_list': True}
    )


@login_required
def profile_follow(request, username):
    """Starts following the author if it is not the user himself."""
    user = request.user
    author = get_object_or_404(User, username=username)
    models.Follow.objects.get_or_create(author=author, user=user)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    """Stops following the author."""
    user = request.user
    follow = models.Follow.objects.filter(author__username=username, user=user)
    follow.delete()
    return redirect('profile', username=username)


def get_ingredients(request, recipe):
    """Processing the transferred ingredients to save the recipe."""
    ingredients = {}
    for key, value in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[value] = request.POST[f'valueIngredient_{num}']
    ingredients_recipe = []
    for name, quantity in ingredients.items():
        ingredient = get_object_or_404(models.Ingredient, name=name)
        ingredients_recipe.append(models.IngredientRecipe(
            recipe=recipe,
            ingredient=ingredient,
            quantity=quantity
        )
        )
    return ingredients_recipe


@login_required
@csrf_protect
def new_recipe(request):
    """Creating a new recipe by an authorized user."""
    form = forms.RecipeForm(
        request.POST or None,
        files=request.FILES or None
    )
    if not form.is_valid():
        return render(
            request,
            'new_recipe.html',
            {'form': form, 'edit': False}
        )
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    ingredients_recipe = get_ingredients(request, recipe)
    models.IngredientRecipe.objects.bulk_create(ingredients_recipe)
    return redirect('index')


@login_required
@csrf_protect
def recipe_edit(request, recipe_id):
    """Editing a new recipe by an authorized user."""
    recipe = get_object_or_404(models.Recipe, id=recipe_id)
    form = forms.RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if not form.is_valid():
        return render(
            request,
            'new_recipe.html',
            {'form': form, 'edit': True}
        )
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    models.IngredientRecipe.objects.filter(recipe=recipe).delete()
    ingredients_recipe = get_ingredients(request, recipe)
    models.IngredientRecipe.objects.bulk_create(ingredients_recipe)
    return redirect('index')


@login_required
def favor_recipes(request):
    """Displays the user's favorite recipes."""
    user = request.user
    latest = models.Recipe.objects.annotate(
        is_favorite=Exists(
            models.FavorRecipe.objects.filter(
                user_id=user.id,
                recipe_id=OuterRef('pk'),
            )),
        is_purchas=Exists(
            models.Purchase.objects.filter(
                user_id=user.id,
                recipe_id=OuterRef('pk'),
            ),
        )).filter(favor_recipe__user=user)
    paginator = Paginator(latest, PAGINATOR_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "favor_recipes.html",
        {"page": page, "paginator": paginator, 'favor': True}
    )


@login_required
def shop_recipes(request):
    """Displays the user's shopping list."""
    user = request.user
    recipes = models.Recipe.objects.filter(shop_recipe__user=user)
    paginator = Paginator(recipes, PAGINATOR_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "shopList.html",
        {"page": page, "paginator": paginator, 'shop': True}
    )


def download_shoplist(request):
    """Uploading a shopping list to a text document."""
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
    """Page 404 output."""
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    """Page 500 output."""
    return render(request, "misc/500.html", status=500)
