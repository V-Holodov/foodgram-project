from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from ..models import FavorRecipe


class CreateFavor(APIView):
    """Add a Recipe to Favorites of a User."""

    def post(self, request, format=None):
        FavorRecipe.objects.get_or_create(
            user=request.user,
            recipe_id=request.data['id'],
        )

        return Response({'success': True}, status=status.HTTP_200_OK)


class DestroyFavor(APIView):
    """Remove a Recipe from User's Favorites."""

    def delete(self, request, pk, format=None):
        FavorRecipe.objects.filter(recipe_id=pk, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
