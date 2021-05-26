from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import FavorRecipe, Follow, Ingredient, Purchase, Recipe
from . import serializers

RESPONSE = JsonResponse({'success': True})
BAD_RESPONSE = JsonResponse(
    {'success': False},
    status=status.HTTP_400_BAD_REQUEST
)


# Объеденил только два класса, третий с подпиской так и не получилось свести
class CreateDestroyBase(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    model = None

    def post(self, request, format=None):
        try:
            self.model.objects.create(
                recipe_id=request.data['id'],
                user=request.user,
            )
            return RESPONSE
        except ValueError:
            return BAD_RESPONSE

    def delete(self, request, pk, format=None):
        favor = self.model.objects.filter(
            recipe_id=pk, user=request.user
        )
        deleted, _ = favor.delete()
        if deleted:
            return RESPONSE
        else:
            return BAD_RESPONSE


class CreateDestroyFavor(CreateDestroyBase):
    """Adding and deleting a recipe to the user's favorites list"""
    model = FavorRecipe


class PurchasesView(CreateDestroyBase):
    """Adding and deleting a recipe to the user's shoplist"""
    model = Purchase


class CreateDestroyFollow(APIView):
    """The functionality of following the author of recipes"""
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, format=None):
        try:
            Follow.objects.create(
                user=request.user,
                idol_id=request.data['id'],
            )
            return RESPONSE
        except ValueError:
            return BAD_RESPONSE

    def delete(self, request, pk, format=None):
        follow = Follow.objects.filter(
            idol_id=pk, user=request.user
        )
        deleted, _ = follow.delete()
        if deleted:
            return RESPONSE
        else:
            return BAD_RESPONSE


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
