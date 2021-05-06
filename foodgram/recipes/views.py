from django.shortcuts import render
from . import models


def index(request):
    latest = models.Recipe.objects.order_by("-pub_date")[:11]
    return render(request, "index.html", {"posts": latest})
