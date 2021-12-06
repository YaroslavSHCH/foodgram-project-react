from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework import viewsets

from .models import Recipe, Tag, Ingredient
from .serializers import (RecipeSerializer,
                          TagSerializer,
                          IngredientViewSerializer)
from .viewsets import ModelCUVDViewSet
from users.pagination import CustomResultsPagination


class RecipeViewSet(ModelCUVDViewSet):
    'Viewset для рецептов'
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = CustomResultsPagination


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    'Viewset для тэгов, только для просмотра'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    'Viewset для ингредиентов, только для просмотра'
    queryset = Ingredient.objects.all()
    serializer_class = IngredientViewSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('name',)
