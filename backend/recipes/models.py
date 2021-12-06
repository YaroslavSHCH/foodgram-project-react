import re
from django.db import models
from django.contrib.auth import get_user_model

from colorfield.fields import ColorField

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        blank=False,
        on_delete=models.CASCADE
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
        related_name='recipes',
        through='IngredientAmount',
        through_fields=['recipe', 'ingredient'],
        verbose_name='Ингредиенты',
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
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        blank=False
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название тега')
    colour = ColorField(verbose_name='Цвет тега', format='hexa')
    slug = models.SlugField(verbose_name='Слаг', max_length=24)

    def __str__(self):
        return self.name


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
        verbose_name='Какой ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='В каком рецепте',
        on_delete=models.CASCADE,
    )
    amount = models.SmallIntegerField(verbose_name='Количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='restrict_double',
            )
        ]
