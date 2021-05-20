from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from typing import Optional
from django.db.models import Exists, OuterRef

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200
    )
    dimension = models.CharField(
        verbose_name='Единица измерения',
        max_length=200
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipes of dishes"""
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
    tag_brekfast = models.BooleanField(default=False)
    tag_lanch = models.BooleanField(default=False)
    tag_dinner = models.BooleanField(default=False)
    cooking_time = models.PositiveIntegerField(
        default=0,
        verbose_name='Время приготовления',
    )
    ingredient = models.ManyToManyField(Ingredient, through='IngredientRecipe')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date', )
        verbose_name = 'Рецепт'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


# class Purchases(models.Model):
#     """Authorized user's shopping list"""
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE,
#         related_name="shoplist"
#     )
#     recipe = models.ForeignKey(
#         Recipe, on_delete=models.CASCADE,
#         related_name="shoplist"
#     )

#     def __str__(self):
#         return f'{self.recipe} в списке покупок у {self.user}'


class FavorRecipe(models.Model):
    """List of the authorized user's favorite recipes"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="favor_recipe"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="favor_recipe"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favor'
                )
        ]

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class Purchas(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shop_recipe')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shop_recipe')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shop'
                )
        ]

    def __str__(self):
        return f'{self.recipe} в покупках у {self.user}'


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
