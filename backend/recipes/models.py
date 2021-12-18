from django.db import models

from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=64, verbose_name='Мера измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор')
    name = models.CharField(max_length=256, verbose_name='Название рецепта')
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение')
    text = models.TextField(verbose_name='text')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe', verbose_name='Ингредиенты')
    tags = models.ManyToManyField('Tag', verbose_name='Тэги')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='related_ingredients', verbose_name='Рецепт')
    amount = models.PositiveIntegerField(verbose_name='Количество ингредиента')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe', 'amount'],
                name='unique_ingredient_recipe')]
        verbose_name = 'Ингредиенты рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'


class Tag(models.Model):
    name = models.CharField(
        max_length=64, unique=True, verbose_name='Название тэга')
    color = models.CharField(max_length=20, unique=True, verbose_name='Цвет')
    slug = models.SlugField(unique=True, verbose_name='Slug')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return '{}, {}'.format(self.name, self.slug)


class Subscribe(models.Model):
    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='following', verbose_name='Кто подписался')
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='follower', verbose_name='На кого подписались')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'follower'], name='unique_follow')]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='user', verbose_name='Пользователь')
    favorite = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorite', verbose_name='Избранное')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favorite'], name='unique_favorite')]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShopingCart(models.Model):
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='customer', verbose_name='Покупатель')
    cart = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='cart', verbose_name='Корзина')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'cart'], name='unique_cart')]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
