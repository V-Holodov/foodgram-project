from django.contrib import admin
from . import models


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author", "tag")
    search_fields = ("name", "author", "tag")
    list_filter = ("name", "author", "tag")
    empty_value_display = "-пусто-"


admin.site.register(models.Recipe, RecipeAdmin)
