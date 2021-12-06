from django.contrib import admin

from .models import Ingredient, Recipe, Tag, IngredientAmount


class IngredientAmountInline(admin.TabularInline):
    model = IngredientAmount
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientAmountInline]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(IngredientAmount)
