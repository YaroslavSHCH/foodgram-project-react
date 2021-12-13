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
from .serializers import (FavoriteAndShoppingCartSerializer,
                          IngredientViewSerializer, RecipeSerializer,
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
    serializer_class = IngredientViewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    filterset_fields = ('name',)
    pagination_class = None


class RecipeViewSet(ModelCUVDViewSet):
    'Viewset for recipe with urls_path methods'
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = CustomResultsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    filterset_fields = (
        'is_favorited',
        'is_in_shopping_cart',
        'author',
        'tags'
    )

    @action(['get', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """View for GET and DELETE recipe to or from favorite"""
        user = self.request.user
        recipe = self.get_object()
        if request.method == 'GET':
            try:
                check_already = recipe.is_favorited.get().is_favorited
            except FavoriteAndShoppingCart.DoesNotExist:
                check_already = False

            if check_already:
                return Response(
                    {'detail': 'Recipe is already in Favorites'},
                    status.HTTP_400_BAD_REQUEST
                )

            FavoriteAndShoppingCart.objects.update_or_create(
                user=user, recipe=recipe,
                defaults={
                    'user': user,
                    'recipe': recipe,
                    'is_favorited': True
                }
            )
            return Response(
                FavoriteAndShoppingCartSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )

        if request.method == 'DELETE':
            favorite_obj = get_object_or_404(
                FavoriteAndShoppingCart,
                recipe=recipe, user=user
            )
            if not favorite_obj.is_in_shopping_cart:
                favorite_obj.delete()
            else:
                favorite_obj.is_favorited = False
                favorite_obj.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET', 'DELETE'],
            detail=True,
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """View for GET and DELETE recipe to or from shoppingcart"""
        user = self.request.user
        recipe = self.get_object()
        if request.method == 'GET':
            try:
                check_already = recipe.is_favorited.get().is_in_shopping_cart
            except FavoriteAndShoppingCart.DoesNotExist:
                check_already = False

            if check_already:
                return Response(
                    {'detail': 'Recipe is already in shopping cart'},
                    status.HTTP_400_BAD_REQUEST)

            FavoriteAndShoppingCart.objects.update_or_create(
                user=user,
                recipe=recipe,
                defaults={
                    'user': user,
                    'recipe': recipe,
                    'is_in_shopping_cart': True
                }
            )
            return Response(
                FavoriteAndShoppingCartSerializer(recipe).data,
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            shopping_cart_obj = get_object_or_404(
                FavoriteAndShoppingCart,
                recipe=recipe, user=user
            )
            if not shopping_cart_obj.is_favorited:
                shopping_cart_obj.delete()
            else:
                shopping_cart_obj.is_in_shopping_cart = False
                shopping_cart_obj.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET'],
            detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request, pk=None):
        """Method exporting shopping list to PDF, used 'reportlab' lib"""
        shopping_list = {}
        user = self.request.user
        recipes = Recipe.objects.filter(
            in_favorites__user=user,
            in_favorites__is_in_shopping_cart=True
        )
        ingredients = recipes.values(
            'ingredients__name',
            'ingredients__measurement_unit').order_by(
            'ingredients__name').annotate(
            ingredients_sum=Sum('ingredients_amount__amount')
        )

        if not recipes:
            return Response('Shopping cart is empty :(')
        for product in ingredients:
            item = product.get('ingredients__name')
            count = str(product.get('ingredients_sum'))+' '+product[
                'ingredients__measurement_unit'
            ]
            shopping_list[item] = count

        return pdf_shopping_list_maker(shopping_list)
