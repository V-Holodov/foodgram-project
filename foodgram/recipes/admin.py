from django.contrib import admin
from . import models


class IngredientRecipeInline(admin.TabularInline):
    model = models.IngredientRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "id")
    list_display_links = ("name",)
    search_fields = ("name", "author")
    list_filter = ("name", "author")
    empty_value_display = "-пусто-"
    inlines = [IngredientRecipeInline]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "dimension")
    list_display_links = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class PurchasAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "recipe")


admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Purchase, PurchasAdmin)
admin.site.register(models.FavorRecipe)
admin.site.register(models.Follow)
