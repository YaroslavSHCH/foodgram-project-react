from django.contrib import admin

from .models import (Ingredient,
                     Recipe,
                     Tag,
                     IngredientAmount,
                     FavoriteAndShoppingCart)


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'colour', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'colour',)
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
    list_filter = ('author', 'name', 'tags', 'ingredients', 'cooking_time')
    empty_value_display = '-'
    inlines = [IngredientAmountInline]

    def get_tags(self, recipe):
        tags_queryset = recipe.list_tags()
        if tags_queryset:
            return list(tags_queryset)
        return None

    def get_favorites(self, recipe):
        favorites_queryset = recipe.in_favorites.count()
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
