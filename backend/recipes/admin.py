from django.contrib import admin

from .models import (
    Favorite, Ingredient, Recipe,
    IngredientRecipe, ShopingCart, Subscribe, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    fields = (
        'author', 'name', 'text', 'tags', 'image', 'cooking_time', 'favorites_count',)
    list_display = ('name', 'author',)
    list_filter = ('name', 'author', 'tags')
    readonly_fields = ('favorites_count',)
    inlines = [
        RecipeIngredientInline
    ]

    def favorites_count(self, obj):
        return Favorite.objects.filter(favorite=obj).count()


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(Tag)
admin.site.register(Subscribe)
admin.site.register(Favorite)
admin.site.register(ShopingCart)
