from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins, permissions
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from ..models import FavorRecipe, Follow, Purchase, Recipe, Ingredient


RESPONSE = JsonResponse({'success': True}, status=status.HTTP_200_OK)
BAD_RESPONSE = JsonResponse(
    {'success': False},
    status=status.HTTP_400_BAD_REQUEST
    )


class CreateDestroyBase(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    create_obj = None
    delete_obj = None

    def post(self, request, format=None):
        try:
            self.create_obj
            return RESPONSE
        except ValueError:
            return BAD_RESPONSE

    def delete(self, request, pk, format=None):
        try:
            favor = self.delete_obj
            favor.delete()
            return RESPONSE
        except ValueError:
            return BAD_RESPONSE


class CreateDestroyFavor(APIView):
    """Adding and deleting a recipe to the user's favorites list"""
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request, format=None):
        try:
            FavorRecipe.objects.create(
                user=request.user,
                recipe_id=request.data['id'],
            )
            return RESPONSE
        except ValueError:
            return BAD_RESPONSE

    def delete(self, request, pk, format=None):
        try:
            favor = FavorRecipe.objects.filter(
                recipe_id=pk, user=request.user
            )
            favor.delete()
            return RESPONSE
        except ValueError:
            return BAD_RESPONSE


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
        try:
            follow = Follow.objects.filter(
                idol_id=pk, user=request.user
            )
            follow.delete()
            return RESPONSE
        except ValueError:
            return BAD_RESPONSE


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
