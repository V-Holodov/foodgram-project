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


class CreateDestroyBase(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    qs = None
    field_name = None

    def post(self, request):
        try:
            pk_filter = self.field_name
            self.qs.create(**{pk_filter: request.data['id']},
                           user=request.user)
            return RESPONSE
        except ValueError:
            return BAD_RESPONSE

    def delete(self, request, pk):
        pk_filter = self.field_name
        obj = self.qs.filter(**{pk_filter: pk},
                             user=request.user)
        deleted, _ = obj.delete()
        if deleted:
            return RESPONSE
        else:
            return BAD_RESPONSE


class CreateDestroyFavor(CreateDestroyBase):
    """Adding and deleting a recipe to the user's favorites list"""
    qs = FavorRecipe.objects.all()
    field_name = 'recipe_id'


class PurchasesView(CreateDestroyBase):
    """Adding and deleting a recipe to the user's shoplist"""
    qs = Purchase.objects.all()
    field_name = 'recipe_id'


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
