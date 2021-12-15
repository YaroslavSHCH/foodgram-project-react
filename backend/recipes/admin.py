from django.contrib import admin

from .models import (FavoriteAndShoppingCart, Ingredient, IngredientAmount,
                     Recipe, Tag)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'color')
    ordering = ('name',)
    empty_value_display = '-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'author',
        'name',
        'text',
        'get_tags',
        'image',
        'cooking_time',
        'get_favorites'
    )
    filter_horizontal = ('tags',)
    search_fields = ('author',)
    list_filter = ('author', 'name', 'tags', 'cooking_time')
    empty_value_display = '-'
    inlines = [IngredientAmountInline]

    def get_tags(self, recipe):
        tags_queryset = recipe.list_tags()
        if tags_queryset:
            return list(tags_queryset)
        return None

    def get_favorites(self, recipe):
        favorites_queryset = recipe.is_favorited.count()
        if favorites_queryset:
            return favorites_queryset
        return None

    get_tags.short_description = 'Теги'
    get_favorites.short_description = 'Добавлено в избранное (раз)'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name', 'measurement_unit',)
    ordering = ('name',)
    empty_value_display = '-'


admin.site.register(FavoriteAndShoppingCart)
admin.site.register(IngredientAmount)
