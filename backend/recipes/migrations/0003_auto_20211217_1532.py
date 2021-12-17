# Generated by Django 3.2.9 on 2021-12-17 12:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Favorite', 'verbose_name_plural': 'Favorites'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ingredient', 'verbose_name_plural': 'Ingredients'},
        ),
        migrations.AlterModelOptions(
            name='ingredientrecipe',
            options={'verbose_name': 'Ingredients of Recipe', 'verbose_name_plural': 'Ingredients of Recipes'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'verbose_name': 'Recipe', 'verbose_name_plural': 'Recipes'},
        ),
        migrations.AlterModelOptions(
            name='shopingcart',
            options={'verbose_name': 'Shopping Cart', 'verbose_name_plural': 'Shopping Carts'},
        ),
        migrations.AlterModelOptions(
            name='subscribe',
            options={'verbose_name': 'Subscribe', 'verbose_name_plural': 'Subscribes'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterField(
            model_name='favorite',
            name='favorite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='recipes.recipe', verbose_name='favorite'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=64, verbose_name='measurement_unit'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=256, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='amount'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', verbose_name='ingredient'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_ingredients', to='recipes.recipe', verbose_name='recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(verbose_name='cooking_time'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipes/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.IngredientRecipe', to='recipes.Ingredient', verbose_name='ingredients'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=256, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipes.Tag', verbose_name='tags'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='shopingcart',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='recipes.recipe', verbose_name='cart'),
        ),
        migrations.AlterField(
            model_name='shopingcart',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='customer'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='follower'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='following'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=20, unique=True, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=64, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='slug'),
        ),
    ]