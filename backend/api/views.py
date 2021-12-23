from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
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
    IngredientSerializer, RecipeReadSerializer, SubscriptionsSerializer)
from .permissions import IsAuthorOrReadOnly
from .filters import RecipeFilter, IngredientFilter
from .paginators import PageNumberPaginatorCustom


class UserViewset(DjoserUserViewSet):
    pagination_class = LimitOffsetPagination

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
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE' and is_subscribed:
            Subscribe.objects.filter(following=user, follower=obj).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=['GET'], permission_classes=[IsAuthenticated],

    )
    def subscriptions(self, request):
        user = request.user
        follows = CustomUser.objects.filter(follower__following=user)
        page = self.paginate_queryset(follows)
        if page is not None:
            serializer = SubscriptionsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SubscriptionsSerializer(follows, many=True)
        return Response(serializer.data)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, )
    filterset_class = IngredientFilter
    search_fields = ('^name',)
    ordering_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = PageNumberPaginatorCustom

    def get_queryset(self):
        qs = Recipe.objects.all()
        if self.request.query_params.get('is_favorited'):
            qs = qs.filter(favorite__user=self.request.user)
        if self.request.query_params.get('is_in_shopping_cart'):
            qs = qs.filter(cart__customer=self.request.user)
        return qs

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
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            serializer = self.get_serializer(obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
