from django_filters import FilterSet, AllValuesMultipleFilter, ModelChoiceFilter

from users.models import MyUser
from recipes.models import Recipe


class RecipeFilter(FilterSet):
    author = ModelChoiceFilter(queryset=MyUser.objects.all())
    tags = AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['tags', 'author']
