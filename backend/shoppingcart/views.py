from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from .models import FavoriteRecipe, ShoppingCart
from .serializers import FavoriteShoppingCartSerializer
from recipes.models import Recipe

User = get_user_model()


@api_view(['GET', 'DELETE'])
def add_to_favorite(request, **kwargs):
    """View function for GET and DELETE recipe to or from favorite of user"""
    if request.method == 'GET':
        recipe_obj = get_object_or_404(Recipe, id=kwargs['recipe_id'])
        # Check existing in Favorite or create
        if FavoriteRecipe.objects.get_or_create(recipe=recipe_obj,
                                                user=request.user)[1]:
            return Response(FavoriteShoppingCartSerializer(recipe_obj).data)

        return Response({'error': 'Рецепт уже есть в избранном'},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        favorite_obj = get_object_or_404(
            FavoriteRecipe, recipe_id=kwargs['recipe_id'])
        favorite_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({'error': 'Не допустимый тип запроса'})


@api_view(['GET', 'DELETE'])
def add_to_shopping_cart(request, **kwargs):
    """View function for GET\DELETE recipe to or from shoppingcart of user"""
    if request.method == 'GET':
        recipe_obj = get_object_or_404(Recipe, id=kwargs['recipe_id'])
        # Check existing in Shoppingcart or create
        if ShoppingCart.objects.get_or_create(recipe=recipe_obj,
                                              user=request.user)[1]:
            return Response(FavoriteShoppingCartSerializer(recipe_obj).data)

        return Response({'error': 'Рецепт уже есть в корзине'},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        cart_obj = get_object_or_404(
            ShoppingCart, recipe_id=kwargs['recipe_id'])
        cart_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({'error': 'Не допустимый тип запроса'})


@api_view(['GET'])
def download_shopping_cart(request, **kwargs):
    pass
