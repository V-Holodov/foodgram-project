from django.db.models import fields
from rest_framework import serializers
from .. import models


class FavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FavorRecipe
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Follow
        fields = '__all__'
