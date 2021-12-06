from django.urls import re_path

from .views import add_to_favorite, add_to_shopping_cart

urlpatterns = [
    re_path(r'(?P<recipe_id>[0-9]+)/favorite/', add_to_favorite),
    re_path(r'(?P<recipe_id>[0-9]+)/shopping_cart/', add_to_shopping_cart)
]
