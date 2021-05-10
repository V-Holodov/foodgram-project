from django.contrib import admin
from . import models


class IngredientRecipeInline(admin.TabularInline):
    model = models.IngredientRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "author")
    list_display_links = ("name",)
    search_fields = ("name", "author", "tag")
    list_filter = ("name", "author", "tag")
    empty_value_display = "-пусто-"
    inlines = [IngredientRecipeInline]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "measure")
    list_display_links = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.ShopList)
admin.site.register(models.FavorRecipe)
admin.site.register(models.Follow)
