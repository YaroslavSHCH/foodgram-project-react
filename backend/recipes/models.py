from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

from colorfield.fields import ColorField

User = get_user_model()


class FavoriteAndShoppingCart(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='is_favorited',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_favorited',
        verbose_name='Пользователь'
    )
    is_favorited = models.BooleanField(
        default=False,
        verbose_name='В избранном'
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='В корзине'
    )

    def __str__(self):
        return f'{self.user.username} {self.recipe.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe',
            )
        ]
        ordering = ['-is_in_shopping_cart', '-is_favorited', 'user']


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        blank=False,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=100,
        blank=False
    )
    image = models.ImageField(
        verbose_name='Изображение блюда',
        blank=False,
    )
    text = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингредиенты',
        related_name='recipes',
        through='IngredientAmount',
        through_fields=['recipe', 'ingredient'],
        blank=False
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Тег',
        related_name='recipes',
        blank=False,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    cooking_time = models.SmallIntegerField(
        verbose_name='Время приготовления',
        blank=False,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.name

    def list_tags(self):
        return self.tags.values_list('name', flat=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'author',
                    'name'
                ],
                name='restrict_double_recipe_author',
            )
        ]
        ordering = ['-pub_date']


class Tag(models.Model):
    name = models.CharField(
        max_length=32,
        unique=True,
        verbose_name='Название тега'
    )
    colour = ColorField(verbose_name='Цвет тега', unique=True, format='hex')
    slug = models.SlugField(verbose_name='Слаг', max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Ингредиент', max_length=200,)
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=16
    )

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredients_amount'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='В каком рецепте',
        on_delete=models.CASCADE,
        related_name='ingredients_amount'
    )
    amount = models.SmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='restrict_double',
            )
        ]
