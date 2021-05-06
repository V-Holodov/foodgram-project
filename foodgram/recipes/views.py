from django.core.paginator import Paginator
from django.shortcuts import render
from . import models


def index(request):
    recipes = models.Recipe.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"recipes": page})
