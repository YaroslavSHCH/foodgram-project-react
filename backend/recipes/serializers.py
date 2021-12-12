from django.db import IntegrityError

from rest_framework import serializers

from .models import (FavoriteAndShoppingCart,
                     Recipe,
                     Tag,
                     Ingredient, IngredientAmount)
from users.serializers import UserSerializer
from .common.decoder import Base64ImageField


class IngredientViewSerializer(serializers.ModelSerializer):
    """Serializer for '/ingredients/' endpoint"""
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']
        read_only_fields = ['id', 'name', 'measurement_unit']


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Serialize and represent ingredients with amount in recipes"""
    class Meta:
        model = IngredientAmount
        fields = ['ingredient', 'amount']
        depth = 1

    def to_representation(self, instance):
        # Delete key 'ingredient' from view, end represent only objects
        rep = super().to_representation(instance)
        ingredient = rep.pop('ingredient')
        serializer = IngredientViewSerializer(ingredient).data
        rep['id'] = serializer['id']
        rep['name'] = serializer['name']
        rep['measurement_unit'] = serializer['measurement_unit']
        rep.move_to_end('amount')
        return rep


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'colour', 'slug']
        read_only_fields = ['id', 'name', 'colour', 'slug']


class FavoriteAndShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
        read_only_fields = ['id', 'name', 'image', 'cooking_time']


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(max_length=None, use_url=True)

    def get_ingredients(self, recipe):
        amount_queryset = IngredientAmount.objects.filter(recipe=recipe)
        serializer = IngredientAmountSerializer(amount_queryset, many=True)
        return serializer.data

    def get_tags(self, recipe):
        tags_queryset = Tag.objects.filter(recipes=recipe)
        serializer = TagSerializer(tags_queryset, many=True)
        return serializer.data

    def get_is_favorited(self, recipe):
        request = self.context.get('request')
        favorited = FavoriteAndShoppingCart.objects.get(
            recipe=recipe,
            user=request.user,
            is_favorited=True
        )
        if not favorited:
            return False
        return True

    def get_is_in_shopping_cart(self, recipe):
        request = self.context.get('request')
        shopping_cart = FavoriteAndShoppingCart.objects.get(
            recipe=recipe,
            user=request.user,
            is_in_shopping_cart=True
        )
        if not shopping_cart:
            return False
        return True

    def validate(self, data):
        data['author'] = self.context['request'].user
        ingredients = self.context['request'].data['ingredients']
        for ingredient in ingredients:
            pk = ingredient['id']
            amount = int(ingredient['amount'])
            ingredient_obj = Ingredient.objects.get(pk=pk)
            if not ingredient_obj:
                detail = {'detail': f'Ингредиента с id={pk} не существует'}
                raise serializers.ValidationError(detail)
            if amount <= 0:
                detail = {'detail': 'Количество не может быть меньше 1'}
                raise serializers.ValidationError(detail)
        data['ingredients'] = ingredients
        tags = self.context['request'].data['tags']
        for tag_id in tags:
            tag_obj = Tag.objects.get(pk=tag_id)
            if not tag_obj:
                detail = {"detail": f"Тег с id={pk} не существует"}
                raise serializers.ValidationError(detail)
        data['tags'] = tags
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        try:
            recipe = Recipe.objects.create(**validated_data)
        except IntegrityError:
            detail = {'detail': 'Вы уже создавали рецепт с таким названием'}
            raise serializers.ValidationError(detail)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            pk = ingredient['id']
            ingredient_obj = Ingredient.objects.get(pk=pk)
            IngredientAmount.objects.create(
                ingredient=ingredient_obj,
                amount=ingredient['amount'],
                recipe=recipe
            )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        for ingredient in ingredients:
            pk = ingredient['id']
            ingredient_obj = Ingredient.objects.get(pk=pk)
            IngredientAmount.objects.update_or_create(
                ingredient=ingredient_obj,
                amount=ingredient['amount'],
                recipe=instance
            )
        for tag_id in tags:
            Tag.objects.get_or_create(recipes=instance, id=tag_id)
        return super().update(instance, validated_data)

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients',
                  'is_in_shopping_cart', 'is_favorited',
                  'name', 'image', 'text', 'cooking_time']
        read_only_fields = ['id', 'author']
