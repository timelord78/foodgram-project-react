from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField

from users.models import CustomUser
from recipes.models import (
    Tag, Ingredient, Recipe, IngredientRecipe,
    Favorite, ShopingCart, Subscribe)


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    class Meta:
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed')
        model = CustomUser

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Subscribe.objects.filter(
            following=request.user, follower=obj).exists()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.CharField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientCreateRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    author = UserSerializer()
    is_favorited = serializers.SerializerMethodField('get_favorited')
    is_in_shopping_cart = serializers.SerializerMethodField(
        'get_shopping_cart')
    ingredients = IngredientRecipeSerializer(
        source='related_ingredients', many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'cooking_time', 'text'
            )

    def get_favorited(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Favorite.objects.filter(
            user=request.user, favorite=obj).exists()

    def get_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return ShopingCart.objects.filter(
            customer=request.user, cart=obj).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    ingredients = IngredientRecipeSerializer(
        many=True, source='related_ingredients')
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')

    @staticmethod
    def parse_ingredients(recipe, data):
        for ingredient_data in data:
            ingredient_current = get_object_or_404(
                Ingredient, pk=ingredient_data['ingredient']['id'])
            IngredientRecipe.objects.create(
                recipe=recipe,
                amount=ingredient_data['amount'],
                ingredient=ingredient_current
            )

    def create(self, validated_data):
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('related_ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.add(*tags)
        self.parse_ingredients(recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.clear()
            instance.tags.add(*tags)
        ingredients_data = validated_data.pop('related_ingredients')
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.parse_ingredients(instance, ingredients_data)
        super().update(instance, validated_data)
        return instance

    def validate(self, data):
        if data['cooking_time'] < 0:
            raise serializers.ValidationError(
                'Укажите корректное время приготовления!')
        ingredients = []
        for ingredient in data['related_ingredients']:
            if ingredient['amount'] < 1:
                raise serializers.ValidationError(
                    'Укажите корректное количество ингредиента!')
            if ingredient['ingredient']['id'] not in ingredients:
                ingredients.append(ingredient['ingredient']['id'])
            else:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться!')
        tags = []
        for tag in data['tags']:
            if tag not in tags:
                tags.append(tag)
            else:
                raise serializers.ValidationError(
                    'Тэги не должны повторяться!')
        return data


class SubscriptionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')
    recipes = RecipeReadSerializer(many=True)

    class Meta:
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed', 'recipes')
        model = CustomUser

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return Subscribe.objects.filter(
            following=request.user, follower=obj).exists()
