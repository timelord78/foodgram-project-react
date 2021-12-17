from django.db import models

from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(max_length=256, verbose_name='name')
    measurement_unit = models.CharField(
        max_length=64, verbose_name='measurement_unit')

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='author')
    name = models.CharField(max_length=256, verbose_name='name')
    image = models.ImageField(upload_to='recipes/', verbose_name='image')
    text = models.TextField(verbose_name='text')
    cooking_time = models.PositiveIntegerField(verbose_name='cooking_time')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe', verbose_name='ingredients')
    tags = models.ManyToManyField('Tag', verbose_name='tags')

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='ingredient')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='related_ingredients', verbose_name='recipe')
    amount = models.PositiveIntegerField(verbose_name='amount')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe', 'amount'], name='unique_ingredient_recipe')]
        verbose_name = 'Ingredients of Recipe'
        verbose_name_plural = 'Ingredients of Recipes'


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='name')
    color = models.CharField(max_length=20, unique=True, verbose_name='color')
    slug = models.SlugField(unique=True, verbose_name='slug')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return '{}, {}'.format(self.name, self.slug)


class Subscribe(models.Model):
    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='following', verbose_name='following')
    follower = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='follower', verbose_name='follower')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'follower'], name='unique_follow')]
        verbose_name = 'Subscribe'
        verbose_name_plural = 'Subscribes'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='user', verbose_name='user')
    favorite = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorite', verbose_name='favorite')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favorite'], name='unique_favorite')]
        verbose_name = 'Favorite'
        verbose_name_plural = 'Favorites'


class ShopingCart(models.Model):
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='customer', verbose_name='customer')
    cart = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='cart', verbose_name='cart')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['customer', 'cart'], name='unique_cart')]
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'
