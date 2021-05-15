from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from ..models import FavorRecipe, Follow


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


class CreateFollow(APIView):
    def post(self, request, format=None):
        Follow.objects.get_or_create(
            user=request.user,
            idol_id=request.data['id'],
        )
        return Response({'success': True}, status=status.HTTP_200_OK)


class DestroyFollow(APIView):
    def delete(self, request, pk, format=None):
        Follow.objects.filter(idol_id=pk, user=request.user).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
