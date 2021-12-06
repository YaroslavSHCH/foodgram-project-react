import csv
from typing import Any, Optional

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Load ingredients from data/ to DB'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        with open('recipes/data/ingredients.csv', encoding='utf-8') as data:
            reader = csv.reader(data)
            for row in reader:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )
