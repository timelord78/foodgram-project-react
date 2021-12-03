from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import fields
from django.utils.safestring import mark_safe

from .models import Favorite, Ingredient, Recipe, IngredientRecipe, ShopingCart, Subscribe, Tag, User



class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class MyUserAdmin(BaseUserAdmin):
    list_display = ('pk', 'username', 'email')
    list_filter = BaseUserAdmin.list_filter + ('email', 'username')


class RecipeIngredientInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('favorites_count',)
    inlines = [
        RecipeIngredientInline,
    ]

    def favorites_count(self, obj):
        return Favorite.objects.filter(favorite=obj).count()
    

    list_display = ('name', 'author',)
    list_filter = ('name', 'author', 'tags')
    fields = ('author', 'name', 'tags', 'text', 'image', 'cooking_time', 'favorites_count',)
    


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientRecipe)
admin.site.register(Tag)
admin.site.register(Subscribe)
admin.site.register(Favorite)
admin.site.register(ShopingCart)
