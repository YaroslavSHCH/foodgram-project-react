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
    is_favorited = BooleanFilter(method='favorite_filter')
    is_in_shopping_cart = BooleanFilter(method='shopping_cart_filter')

    def shopping_cart_filter(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(
                is_favorited__user=self.request.user,
                is_favorited__is_in_shopping_cart=value
            )
        return queryset

    def favorite_filter(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(
                is_favorited__user=self.request.user,
                is_favorited__is_favorited=value
            )
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ['name']
