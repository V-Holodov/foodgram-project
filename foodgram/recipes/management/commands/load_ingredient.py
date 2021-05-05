from django.core.management.base import BaseCommand
from recipes.models import Ingredient
import csv


class Command(BaseCommand):
    help = 'Load ingredient'

    def handle(self, *args, **kwargs):
        pass
