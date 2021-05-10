from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<int:recipe_id>", views.recipe_detail, name="recipe_detail"),
    path("author/<int:author_id>", views.author_page, name="author_page"),
    path("follow/", views.follow_list, name="follow_list"),
]
