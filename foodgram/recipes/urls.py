from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter
from . import views
from .api.views import (CreateFavor, DestroyFavor, CreateFollow, DestroyFollow,
                        PurchasesViewSet, PurchasesView)


views_patterns = [
    path("", views.index, name="index"),
    path("tagadd/<str:tag>", views.index_add_tag, name="index_add_tag"),
    path("tagdel/<str:tag>", views.index_del_tag, name="index_del_tag"),
    path("recipe/<int:recipe_id>", views.recipe_detail, name="recipe_detail"),
    path("author/<int:author_id>", views.author_page, name="author_page"),
    path("follow/", views.follow_list, name="follow_list"),
    path("new/", views.new_recipe, name="new_recipe"),
    path('favor/', views.favor_recipes, name='favor_recipes'),
    path('shop/', views.shop_recipes, name='shop_recipes'),
    path('shop/download/', views.download_shoplist, name='download_shoplist'),

]

# router = SimpleRouter()
# router.register('purchases', PurchasesViewSet, basename='purchases')

api_patterns = [
    path('favorites/', CreateFavor.as_view()),
    path('favorites/<int:pk>/', DestroyFavor.as_view()),
    path('subscriptions/', CreateFollow.as_view()),
    path('subscriptions/<int:pk>/', DestroyFollow.as_view()),
    path('purchases/<int:pk>/', PurchasesView.as_view()),
    path('purchases/', PurchasesView.as_view()),
]

# api_patterns += router.urls

urlpatterns = [
    path('', include(views_patterns)),
    path('api/', include(format_suffix_patterns(api_patterns))),
]
