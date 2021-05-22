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

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

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
    tag_brekfast = models.BooleanField(default=False, verbose_name='Завтрак')
    tag_lanch = models.BooleanField(default=False, verbose_name='Обед')
    tag_dinner = models.BooleanField(default=False, verbose_name='Ужин')
    cooking_time = models.PositiveIntegerField(
        validators=(
            MinValueValidator(limit_value=1),
        ),
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
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт для ингредиента'
        )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент для рецепта'
        )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество ингредиента'
        )

    class Meta:
        verbose_name = 'Связь ингредиента и рецепта'
        verbose_name_plural = 'Связи ингредиентов и рецептов'


class FavorRecipe(models.Model):
    """List of the authorized user's favorite recipes"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="favor_recipe",
        verbose_name='Пользователь избранного рецепта'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name="favor_recipe",
        verbose_name='Рецепт у избранного пользователя'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favor'
                )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shop_recipe',
        verbose_name='Хозяин корзины покупок'
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shop_recipe',
        verbose_name='Рецепт в корзине пользователя'
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shop'
                )
        ]

    class Meta:
        verbose_name = 'Рецепт в корзине покупок'
        verbose_name_plural = 'Рецепты в корзине покупок'

    def __str__(self):
        return f'{self.recipe} в покупках у {self.user}'


class Follow(models.Model):
    """Relationship between an authorized user and their following"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
        )
    idol = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mentor',
        verbose_name='На кого подписан пользователь')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'idol'],
                name='unique_follow'
                ),
            # models.CheckConstraint(
            #     check=~models.Q(user__exact='idol'),
            #     name='no_following_yourself'
            #     )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.idol}'
