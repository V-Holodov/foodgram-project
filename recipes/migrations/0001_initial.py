# Generated by Django 2.2.19 on 2021-05-29 20:04

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название ингредиента')),
                ('dimension', models.CharField(max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество ингредиента')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Ingredient', verbose_name='ингредиент для рецепта')),
            ],
            options={
                'verbose_name': 'Связь ингредиента и рецепта',
                'verbose_name_plural': 'Связи ингредиентов и рецептов',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название рецепта')),
                ('image', models.ImageField(upload_to='recipes/', verbose_name='Загрузить фото')),
                ('description', models.TextField(verbose_name='Описание')),
                ('tag_breakfast', models.BooleanField(default=False, verbose_name='Завтрак')),
                ('tag_lunch', models.BooleanField(default=False, verbose_name='Обед')),
                ('tag_dinner', models.BooleanField(default=False, verbose_name='Ужин')),
                ('cooking_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1)], verbose_name='Время приготовления')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL)),
                ('ingredient', models.ManyToManyField(through='recipes.IngredientRecipe', to='recipes.Ingredient')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_recipe', to='recipes.Recipe', verbose_name='Рецепт в корзине пользователя')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_recipe', to=settings.AUTH_USER_MODEL, verbose_name='Хозяин корзины покупок')),
            ],
            options={
                'verbose_name': 'Рецепт в корзине покупок',
                'verbose_name_plural': 'Рецепты в корзине покупок',
            },
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='рецепт для ингредиента'),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentor', to=settings.AUTH_USER_MODEL, verbose_name='На кого подписан пользователь')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.CreateModel(
            name='FavorRecipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favor_recipe', to='recipes.Recipe', verbose_name='Рецепт у избранного пользователя')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favor_recipe', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь избранного рецепта')),
            ],
            options={
                'verbose_name': 'Избранный рецепт',
                'verbose_name_plural': 'Избранные рецепты',
            },
        ),
        migrations.AddConstraint(
            model_name='purchase',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shop'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'idol'), name='unique_follow'),
        ),
        migrations.AddConstraint(
            model_name='favorrecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favor'),
        ),
    ]
