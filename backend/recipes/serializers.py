from django.db import IntegrityError
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.serializers import UserSerializer
from .common.validation_errors import DETAILS
from .models import Ingredient, IngredientAmount, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for '/ingredients/' endpoint"""
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']
        read_only_fields = ['id', 'name', 'measurement_unit']


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Serialize and represent ingredients with amount in recipes"""
    id = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='id',
        queryset=Ingredient.objects.all()
    )
    name = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='measurement_unit',
        read_only=True
    )

    class Meta:
        model = IngredientAmount
        fields = ['id', 'name', 'amount', 'measurement_unit']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']
        read_only_fields = ['id', 'name', 'color', 'slug']


class FavoriteAndShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']
        read_only_fields = ['id', 'name', 'image', 'cooking_time']


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    def get_is_favorited(self, recipe):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return recipe.is_favorited.filter(
            user=request.user,
            is_favorited=True
        ).exists()

    def get_is_in_shopping_cart(self, recipe):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return recipe.is_favorited.filter(
            user=request.user,
            is_in_shopping_cart=True
        ).exists()

    def to_representation(self, instance):
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(instance)

    def validate(self, data):
        ingredients = data['ingredients']
        ingredients_dict = {}
        for ingredient in ingredients:
            ingredient_obj = ingredient['ingredient']
            amount = ingredient['amount']
            pk = ingredient_obj.pk
            if amount <= 0:
                raise serializers.ValidationError(DETAILS['amount'])
            if ingredients_dict.get(pk):
                raise serializers.ValidationError(DETAILS['unique'])
            ingredients_dict[pk] = (ingredient_obj, amount)
        data['ingredients'] = ingredients_dict
        tags = data['tags']
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(DETAILS['tags'])
            tags_list.append(tag)
        data['tags'] = tags
        cooking_time = data['cooking_time']
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(DETAILS['cooking_time'])

        return data

    def ingredients_create_or_update(self, method, ingredients, recipe):
        method_actions = {
            'create': IngredientAmount.objects.create,
            'update': IngredientAmount.objects.update_or_create
        }
        for ingredient, amount in ingredients.values():
            method_actions[method](
                ingredient=ingredient,
                recipe=recipe,
                amount=amount
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        try:
            recipe = Recipe.objects.create(**validated_data)
        except IntegrityError:
            detail = {'detail': '???? ?????? ?????????????????? ???????????? ?? ?????????? ??????????????????'}
            raise serializers.ValidationError(detail)

        self.ingredients_create_or_update('create', ingredients, recipe)
        recipe.tags.add(*tags)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.ingredients_create_or_update('update', ingredients, instance)
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.add(*tags)
        super().update(instance, validated_data)
        return instance

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients',
                  'is_in_shopping_cart', 'is_favorited',
                  'name', 'image', 'text', 'cooking_time']
        read_only_fields = ['id', 'author']
