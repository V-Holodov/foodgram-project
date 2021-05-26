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


# class CreateDestroyBase(APIView):
#     permission_classes = [permissions.IsAuthenticated, ]
#     model = None
#     relat_model = None

#     def post(self, request, format=None):
#         try:
#             FavorRecipe.objects.create(
#                 user=request.user,
#                 recipe_id=request.data['id'],
#             )
#             return RESPONSE
#         except ValueError:
#             return BAD_RESPONSE

#     def delete(self, request, pk, format=None):
#         favor = FavorRecipe.objects.filter(
#             recipe_id=pk, user=request.user
#         )
#         deleted, _ = favor.delete()
#         if deleted:
#             return RESPONSE
#         else:
#             return BAD_RESPONSE


# class CreateDestroyFavor(CreateDestroyBase):
#     """Adding and deleting a recipe to the user's favorites list"""
#     model = FavorRecipe
#     field = FavorRecipe.recipe.id


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
        favor = FavorRecipe.objects.filter(
            recipe_id=pk, user=request.user
        )
        deleted, _ = favor.delete()
        if deleted:
            return RESPONSE
        else:
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
        follow = Follow.objects.filter(
            idol_id=pk, user=request.user
        )
        deleted, _ = follow.delete()
        if deleted:
            return RESPONSE
        else:
            return BAD_RESPONSE


class PurchasesView(APIView):

    def delete(self, request, *args, **kwargs):
        try:
            recipe_id = self.kwargs.get('pk')
            purchas = Purchase.objects.filter(user=self.request.user,
                                              recipe=recipe_id)
            purchas.delete()
            return RESPONSE
        except ValueError:
            return BAD_RESPONSE

    def post(self, request):
        try:
            recipe_id = request.data.get('id')
            recipe = get_object_or_404(Recipe, id=recipe_id)
            Purchase.objects.get_or_create(user=request.user, recipe=recipe)
            return RESPONSE
        except ValueError:
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
