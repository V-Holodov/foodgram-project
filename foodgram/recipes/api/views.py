from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins, permissions
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from ..models import FavorRecipe, Follow, Purchase, Recipe, Ingredient


class CreateDestroyFavor(APIView):
    """Adding and deleting a recipe to the user's favorites list"""
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, format=None):
        FavorRecipe.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )
        return JsonResponse({'success': True})

    def delete(self, request, pk, format=None):
        get_object_or_404(
            FavorRecipe, recipe_id=pk, user=request.user
        ).delete()
        return JsonResponse({'success': True})


class CreateDestroyFollow(APIView):
    """The functionality of following the author of recipes"""
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, format=None):
        Follow.objects.get_or_create(
            user=request.user,
            idol_id=request.data['id'],
        )
        return JsonResponse({'success': True})

    def delete(self, request, pk, format=None):
        get_object_or_404(Follow, idol_id=pk, user=request.user).delete()
        return JsonResponse({'success': True})


class PurchasesViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.ViewSet,
):
    serializer_class = serializers.PurchasesSerializer

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        recipe_id = self.request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)


class PurchasesView(APIView):

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('pk')
        purchas = Purchase.objects.filter(user=self.request.user,
                                          recipe=recipe_id)
        purchas.delete()
        return Response({'success': True})

    def post(self, request):
        recipe_id = request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Purchase.objects.get_or_create(user=request.user, recipe=recipe)
        return Response({'success': True})


class IngredientView(APIView):
    def get(self, request):
        ingredients = Ingredient.objects.filter(
            name__startswith=request.query_params.get('query')
        )
        list_ingredients = [
            {
                'title': ingredient.name,
                'dimension': ingredient.dimension
            }for ingredient in ingredients
        ]
        return Response(list_ingredients)
