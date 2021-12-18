from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.http import HttpResponse
from djoser.views import UserViewSet as DjoserUserViewSet
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import (
    Tag, Ingredient, Recipe, Favorite, ShopingCart, Subscribe)
from users.models import CustomUser
from .serializers import (
    RecipeWriteSerializer, TagSerializer,
    IngredientSerializer, RecipeReadSerializer)
from .permissions import IsAuthorOrReadOnly
from .filters import RecipeFilter


class UserViewset(DjoserUserViewSet):

    @action(
        detail=True, methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        obj = self.get_object()
        is_subscribed = Subscribe.objects.filter(
            following=user, follower=obj).exists()
        if request.method == 'GET' and not is_subscribed:
            Subscribe.objects.create(following=user, follower=obj)
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE' and is_subscribed:
            Subscribe.objects.filter(following=user, follower=obj).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=['GET'], permission_classes=[IsAuthenticated],
        pagination_class=LimitOffsetPagination
    )
    def subscriptions(self, request):
        user = request.user
        queryset = CustomUser.objects.filter(follower__following=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True, methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        obj = self.get_object()
        favorite = Favorite.objects.filter(user=user, favorite=obj).exists()
        if request.method == 'GET' and not favorite:
            Favorite.objects.create(user=user, favorite=obj)
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE' and favorite:
            Favorite.objects.filter(user=user, favorite=obj).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True, methods=['GET', 'DELETE'],
        permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        obj = self.get_object()
        in_cart = ShopingCart.objects.filter(customer=user, cart=obj).exists()
        if request.method == 'GET' and not in_cart:
            ShopingCart.objects.create(customer=user, cart=obj)
            return Response(status=status.HTTP_201_CREATED)
        if request.method == 'DELETE' and in_cart:
            ShopingCart.objects.filter(customer=user, cart=obj).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        in_cart = Recipe.objects.filter(cart__customer=user)
        queryset = in_cart.values_list(
            'ingredients__name',
            'related_ingredients__amount',
            'ingredients__measurement_unit')
        text = 'Ваш список покупок: \n'
        for ingredient in queryset:
            text += f'{str(ingredient)} \n'
        response = HttpResponse(text, 'Content-Type: application/txt')
        response['Content-Disposition'] = 'attachment; filename="wishlist"'
        return response
