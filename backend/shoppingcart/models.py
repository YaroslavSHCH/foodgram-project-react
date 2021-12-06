from django.db import models
from django.contrib.auth import get_user_model

from recipes.models import Recipe

User = get_user_model()


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'shopping_cart')


class FavoriteRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_recipe')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='restrict_many_for_one_recipe_favorite',
            )
        ]
