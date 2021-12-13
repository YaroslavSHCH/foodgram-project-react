# Generated by Django 3.0.5 on 2021-12-12 17:53

import colorfield.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteAndShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favorited', models.BooleanField(default=False, verbose_name='В избранном')),
                ('is_in_shopping_cart', models.BooleanField(default=False, verbose_name='В корзине')),
            ],
            options={
                'ordering': ['-is_in_shopping_cart', '-is_favorited', 'user'],
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Ингредиент')),
                ('measurement_unit', models.CharField(max_length=16, verbose_name='Единица измерения')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='IngredientAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название рецепта')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение блюда')),
                ('text', models.TextField(verbose_name='Описание рецепта')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('cooking_time', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='Название тега')),
                ('colour', colorfield.fields.ColorField(default='#FFFFFF', max_length=18, unique=True, verbose_name='Цвет тега')),
                ('slug', models.SlugField(max_length=32, unique=True, verbose_name='Слаг')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
