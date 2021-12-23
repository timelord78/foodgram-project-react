from django_filters import (
    FilterSet, AllValuesMultipleFilter, CharFilter)

from recipes.models import Recipe, Ingredient


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')


class IngredientFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Ingredient
        fields = ('name',)
