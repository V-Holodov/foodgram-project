from django.shortcuts import render
from . import models


def index(request):
    recipes = models.Recipe.objects.all()
    return render(request, "index.html", {"recipes": recipes})
