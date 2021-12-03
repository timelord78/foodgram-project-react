from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    measurement_unit = models.CharField(max_length=64)

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes')
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    text = models.TextField()
    cooking_time = models.PositiveIntegerField()
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()


class Tag(models.Model):
    name = models.CharField(max_length=64)
    color = models.CharField(max_length=20)
    slug = models.SlugField()

    def __str__(self):
        return '{}, {}'.format(self.name, self.slug)


class Subscribe(models.Model):
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['following', 'follower'], name='unique_follow')]


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    favorite = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'favorite'], name='unique_favorite')]


class ShopingCart(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='customer')
    cart = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='cart')
