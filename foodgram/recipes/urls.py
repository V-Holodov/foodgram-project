from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter
from . import views
from .api.views import (CreateDestroyFavor, CreateDestroyFollow,
                        PurchasesView, IngredientView)


views_patterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tagadd/<str:tag>/', views.index_add_tag, name='index_add_tag'),
    path('tagdel/<str:tag>/', views.index_del_tag, name='index_del_tag'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path(
        'author/<int:author_id>/',
        views.ProfileView.as_view(),
        name='author_page'
        ),
    path('follow/', views.follow_list, name='follow_list'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('edit/<int:recipe_id>/', views.recipe_edit, name='recipe_edit'),
    path('favor/', views.FavoriteView.as_view(), name='favor_recipes'),
    path('shop/', views.shop_recipes, name='shop_recipes'),
    path('shop/download/', views.download_shoplist, name='download_shoplist'),

]


api_patterns_v1 = [
    path('favorites/', CreateDestroyFavor.as_view()),
    path('favorites/<int:pk>/', CreateDestroyFavor.as_view()),
    path('subscriptions/', CreateDestroyFollow.as_view()),
    path('subscriptions/<int:pk>/', CreateDestroyFollow.as_view()),
    path('purchases/<int:pk>/', PurchasesView.as_view()),
    path('purchases/', PurchasesView.as_view()),
    path('ingredients/', IngredientView.as_view()),
]


urlpatterns = [
    path('', include(views_patterns)),
    path('api/v1/', include(format_suffix_patterns(api_patterns_v1))),
]
