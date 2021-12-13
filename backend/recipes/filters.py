from django_filters import (BooleanFilter, CharFilter, FilterSet,
                            ModelMultipleChoiceFilter, NumberFilter)

from .models import Ingredient, Recipe, Tag


class RecipeFilter(FilterSet):
    author = NumberFilter(
        field_name='author__id',
        lookup_expr='exact'
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = BooleanFilter(
        field_name='is_favorited__is_favorited'
    )
    is_in_shopping_cart = BooleanFilter(
        field_name='is_favorited__is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name']
