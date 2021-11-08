from django.db import models
from django.contrib.auth import get_user_model

from colorfield.fields import ColorField

User = get_user_model()


class Measure(models.TextChoices):
    KG = 'кг', 'киллограмм'
    GRAM = 'г', 'грамм'
    LITER = 'л', 'литер'  
    MILLILITER = 'мл', 'миллилитер'
    TEA_SPOON = 'ч.л.', 'чайная ложка'
    SPOON = 'ст.л', 'столовая ложка'
    ITEM = 'шт.', 'штук'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        blank=False,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=100,
        blank=False
    )
    image = models.ImageField(verbose_name='Изображение блюда', blank=True)
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField('Ingredient', related_name='recipes')
    tag = models.ManyToManyField(
        'Tag',
        verbose_name='Тег',
        related_name='recipes',
        blank=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True)
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        blank=False
    )

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-pub_date']


class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название тега')
    colour = ColorField(format='hexa')
    slug = models.SlugField('Slug', name='TagSlug')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Ингредиент', max_length=200,)
    amount = models.DecimalField(
        verbose_name='Количество',
        decimal_places=1,
        max_digits=4
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=16,
        choices=Measure.choices
    )

    def __str__(self):
        return self.name
