from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.pagination import CustomResultsPagination
from .common.pdfmaker import pdf_shopping_list_maker
from .filters import IngredientFilter, RecipeFilter
from .models import FavoriteAndShoppingCart, Ingredient, Recipe, Tag
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteAndShoppingCartSerializer,
                          IngredientSerializer, RecipeSerializer,
                          TagSerializer)
from .viewsets import ModelCUVDViewSet


class TagViewSet(ReadOnlyModelViewSet):
    'Viewset для тэгов, только для просмотра'
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    'Viewset для ингредиентов, только для просмотра'
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    filterset_fields = ('name',)
    pagination_class = None


class RecipeViewSet(ModelCUVDViewSet):
    'Viewset for recipe with urls_path methods'
    queryset = Recipe.objects.prefetch_related('ingredients').all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = CustomResultsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    filterset_fields = (
        'is_favorited',
        'is_in_shopping_cart',
        'author',
        'tags'
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def favorite_shopping_cart_add(self, defaults):
        recipe = defaults.get('recipe')
        user = defaults.get('user')
        if defaults.get('is_favorited'):
            try:
                check_already = recipe.is_favorited.get().is_favorited
            except FavoriteAndShoppingCart.DoesNotExist:
                check_already = False
            detail = {'detail': 'Рецепт уже в избранном'}

        if defaults.get('is_in_shopping_cart'):
            try:
                check_already = recipe.is_favorited.get().is_in_shopping_cart
            except FavoriteAndShoppingCart.DoesNotExist:
                check_already = False
            detail = {'detail': 'Рецепт уже в корзине'}

        if check_already:
            return Response(detail, status.HTTP_400_BAD_REQUEST)

        FavoriteAndShoppingCart.objects.update_or_create(
            recipe=recipe,
            user=user,
            defaults=defaults
        )
        return Response(
            FavoriteAndShoppingCartSerializer(recipe).data,
            status=status.HTTP_201_CREATED
        )

    def favorite_shopping_cart_delete(self, defaults):
        favorite_obj = get_object_or_404(
            FavoriteAndShoppingCart,
            recipe=defaults['recipe'], user=defaults['user']
        )
        if defaults.get('is_favorited'):
            favorite_obj.is_favorited = False
        if defaults.get('is_in_shopping_cart'):
            favorite_obj.is_in_shopping_cart = False

        favorite_obj.save()
        if favorite_obj.is_favorited == favorite_obj.is_in_shopping_cart:
            favorite_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['get', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """View for GET and DELETE recipe to or from favorite"""
        defaults = {
            'user': self.request.user,
            'recipe': self.get_object(),
            'is_favorited': True
        }
        if request.method == 'GET':
            return self.favorite_shopping_cart_add(defaults=defaults)
        if request.method == 'DELETE':
            return self.favorite_shopping_cart_delete(defaults=defaults)

    @action(methods=['GET', 'DELETE'],
            detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """View for GET and DELETE recipe to or from shoppingcart"""
        defaults = {
            'user': self.request.user,
            'recipe': self.get_object(),
            'is_in_shopping_cart': True
        }
        if request.method == 'GET':
            return self.favorite_shopping_cart_add(defaults=defaults)
        if request.method == 'DELETE':
            return self.favorite_shopping_cart_delete(defaults=defaults)

    @action(methods=['GET'],
            detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request, pk=None):
        """Method exporting shopping list to PDF, used 'reportlab' lib"""
        shopping_list = {}
        user = self.request.user
        recipes = Recipe.objects.filter(
            is_favorited__user=user,
            is_favorited__is_in_shopping_cart=True
        )
        ingredients = recipes.values(
            'ingredients__ingredient__name',
            'ingredients__ingredient__measurement_unit').order_by(
            'ingredients__ingredient__name').annotate(
            ingredients_sum=Sum('ingredients__amount')
        )
        if not recipes:
            return Response('Ваша корзина пуста')
        for product in ingredients:
            item = product.get('ingredients__ingredient__name')
            count = str(product.get('ingredients_sum')) + ' ' + product[
                'ingredients__ingredient__measurement_unit'
            ]
            shopping_list[item] = count
        return pdf_shopping_list_maker(shopping_list)
