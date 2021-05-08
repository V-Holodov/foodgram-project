from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe/<int:id>", views.recipe_detail, name="recipe_detail"),
]
