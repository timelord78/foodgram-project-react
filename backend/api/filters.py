from django_filters import FilterSet, AllValuesMultipleFilter, ModelChoiceFilter

from users.models import CustomUser
from recipes.models import Recipe


class RecipeFilter(FilterSet):
    author = ModelChoiceFilter(queryset=CustomUser.objects.all())
    tags = AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['tags', 'author']

    def filter_queryset(self, request):
        qs = Recipe.objects.all()
        if self.request.query_params.get('is_favorited'):
            qs = qs.filter(favorite__user=self.request.user)
        if self.request.query_params.get('is_in_shopping_cart'):
            qs = qs.filter(cart__customer=self.request.user)
        return qs
