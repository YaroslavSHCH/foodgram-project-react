from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from recipes.models import Recipe

from .models import Follow, User


class SimpleRecipeSerializer(serializers.ModelSerializer):
    """Serializer for user list view, with short fieldset"""
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        """Cheking subscription"""
        user = self.context.get('request').user
        if user.is_authenticated:
            try:
                user = self.context.get('request').user
                follow_obj = Follow.objects.get(
                    user=user,
                    following=obj
                )
            except Follow.DoesNotExist:
                follow_obj = False

            return bool(follow_obj)

        return False

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        ]


class SubscribeSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        recipes_queryset = Recipe.objects.filter(author=obj)
        serializer = SimpleRecipeSerializer(recipes_queryset, many=True)
        return serializer.data

    class Meta(UserSerializer.Meta):
        model = UserSerializer.Meta.model
        fields = UserSerializer.Meta.fields + ['recipes']


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
