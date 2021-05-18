from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from ..models import FavorRecipe, Follow, Purchas, Recipe, Ingredient


class CreateFavor(APIView):
    """Add a Recipe to Favorites of a User."""

    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, format=None):
        FavorRecipe.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class DestroyFavor(APIView):
    """Remove a Recipe from User's Favorites."""

    permission_classes = [permissions.IsAuthenticated, ]

    def delete(self, request, pk, format=None):
        FavorRecipe.objects.filter(recipe_id=pk, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class CreateFollow(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, format=None):
        Follow.objects.get_or_create(
            user=request.user,
            idol_id=request.data['id'],
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class DestroyFollow(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def delete(self, request, pk, format=None):
        Follow.objects.filter(idol_id=pk, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)


class PurchasesViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.ViewSet,
):
    serializer_class = serializers.PurchasesSerializer

    def get_queryset(self):
        return Purchas.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        recipe_id = self.request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)


class PurchasesView(APIView):

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('pk')
        purchas = Purchas.objects.filter(user=self.request.user,
                                         recipe=recipe_id)
        purchas.delete()
        return Response({'success': True})

    def post(self, request):
        recipe_id = request.data.get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        Purchas.objects.get_or_create(user=request.user, recipe=recipe)
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
