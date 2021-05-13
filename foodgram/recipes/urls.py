from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views
from .api.views import CreateFavor, DestroyFavor

views_patterns = [
    path("", views.index, name="index"),
    path("tag/<str:tag>", views.tag_index, name="tag_index"),
    path("recipe/<int:recipe_id>", views.recipe_detail, name="recipe_detail"),
    path("author/<int:author_id>", views.author_page, name="author_page"),
    path("follow/", views.follow_list, name="follow_list"),
    path("new/", views.new_recipe, name="new_recipe"),
    path('favor/', views.favor_recipes, name='favor_recipes'),
    path('shop/', views.shop_recipes, name='shop_recipes'),
]

api_patterns = [
    path('favorites/', CreateFavor.as_view()),
    path('favorites/<int:pk>/', DestroyFavor.as_view()),
]

urlpatterns = [
    path('', include(views_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns))),
]
