from rest_framework import serializers

from .models import Recipe, Tag, Ingredient, IngredientAmount
from .specials import Base64ImageField
from users.serializers import UserSerializer


class IngredientViewSerializer(serializers.ModelSerializer):
    """Serializer for '/ingredients/' endpoints"""
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
        # Expand 'ingredient' dict, without key itself
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


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(slug_field='id', queryset=Tag.objects.all(), many=True)
    image = Base64ImageField(max_length=None, use_url=True)

    def get_ingredients(self, recipe):
        amount_queryset = IngredientAmount.objects.filter(recipe=recipe)
        serializer = IngredientAmountSerializer(amount_queryset, many=True)
        return serializer.data

# TODO Представления во вьюсете, создание и валидация в сериалайзере
    def to_representation(self, instance):
        """Represent 'tags' field in response for full view"""
        rep = super().to_representation(instance)
        rep['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return rep

    def validate(self, data):
        data['author'] = self.context['request'].user
        data['ingredients'] = self.context['request'].data['ingredients']
        data['tags'] = self.context['request'].data['tags']
        return data

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            pk = ingredient['id']
            try:
                ingredient_obj = Ingredient.objects.get(pk=pk)
            except Ingredient.DoesNotExist:
                detail = {"detail": f"Ингредиента с id={pk} не существует"}
                raise serializers.ValidationError(detail)
            IngredientAmount.objects.create(
                ingredient=ingredient_obj,
                amount=ingredient['amount'],
                recipe=recipe
            )

        return recipe

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time']
        read_only_fields = ['id', 'author']
