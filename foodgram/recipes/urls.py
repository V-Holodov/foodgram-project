from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<int:recipe_id>", views.recipe_detail, name="recipe_detail"),
    path("author/<int:author_id>", views.author_page, name="author_page"),
    path("follow/", views.follow_list, name="follow_list"),
    path("new/", views.new_recipe, name="new_recipe"),
    path('favor/', views.favor_recipes, name='favor_recipes')
]
