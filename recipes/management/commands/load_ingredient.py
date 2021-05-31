import csv
import os

from django.core.management.base import BaseCommand

from config.settings import BASE_DIR
from recipes.models import Ingredient

CSV_FILE_PATH = os.path.join(BASE_DIR, 'ingredients.csv')


class Command(BaseCommand):
    help = 'Load ingredient'

    def handle(self, *args, **kwargs):
        with open(CSV_FILE_PATH) as file:
            reader = csv.reader(file)
            for row in reader:
                name, dimension = row
                Ingredient.objects.get_or_create(
                    name=name, dimension=dimension)
            print("Ингредиенты загружены")
