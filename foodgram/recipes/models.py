from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200
    )
    measure = models.CharField(
        verbose_name='Единица измерения',
        max_length=200
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipes of dishes"""
    BREAKFAST = 'B'
    LANCH = 'L'
    DINNER = 'D'
    MEALTIME_CHOICES = [
        (BREAKFAST, 'Завтрак'),
        (LANCH, 'Обед'),
        (DINNER, 'Ужин')
        ]
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="recipe"
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Загрузить фото',
        upload_to='recipes/',
        blank=True, null=True
    )
    description = models.TextField(verbose_name='Описание')
    tag = MultiSelectField(
        choices=MEALTIME_CHOICES,
        verbose_name='Теги')
    cooking_time = models.PositiveIntegerField(
        default=0,
        verbose_name='Время приготовления',
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text=('Укажите адрес для страницы группы. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания'),
        max_length=70, unique=True
    )
    ingredient = models.ManyToManyField(Ingredient, through='IngredientRecipe')
    # shoplist = models.ManyToManyField(
    #     'Shoplist', related_name="recipe", blank=True
    #     )
    # favor_recipe = models.ManyToManyField(
    #     'FavorRecipe', related_name="recipe", blank=True
    #     )

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class ShopList(models.Model):
    """Authorized user's shopping list"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="shoplist"
    )


class FavorRecipe(models.Model):
    """List of the authorized user's favorite recipes"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="favor_recipe"
    )


class Follow(models.Model):
    """Relationship between an authorized user and their following"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    idol = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mentor')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'idol'],
                name='unique_follow'
                )
        ]
