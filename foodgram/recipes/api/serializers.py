from django.db.models import fields
from rest_framework import serializers
from .. import models


class FavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FavorRecipe
        fields = '__all__'
