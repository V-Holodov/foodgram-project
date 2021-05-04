from django.db import models
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


class Recipe(models.Model):
    """Recipes of dishes"""
    BREAKFAST = 'B', 'Завтрак'
    LANCH = 'L', 'Обед'
    DINNER = 'D', 'Ужин'
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
        upload_to='recipe/',
        blank=True, null=True
    )
    description = models.TextField(verbose_name='Описание')
    tag = MultiSelectField(
        choices=MEALTIME_CHOICES,
        verbose_name='Теги')
    cooking_time = models.IntegerField(
        default=0,
        verbose_name='Время приготовления',
        # validators=(
        #     MinValueValidator(limit_value=0))
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        help_text=('Укажите адрес для страницы группы. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания'),
        max_length=70, unique=True
    )
    ingredient = models.ManyToManyField('Ingredient', related_name="recipe")
    shoplist = models.ManyToManyField('Shoplist', related_name="recipe")
    favor_recipe = models.ManyToManyField('FavorRecipe', related_name="recipe")


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
        related_name="shoplist"
    )
