from django.db import models
from pytils.translit import slugify

from users.models import User

from .validators import validate_positive


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название продукта',
        help_text='Введите короткое название продукта',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения',
        max_length=200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self) -> str:
        return f'{self.name}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE,
        related_name='recipe_ingredients',
        verbose_name='Рецепт'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='ingredients_recipe',
        verbose_name='Ингредиент'
    )
    amount = models.FloatField(validators=[validate_positive],
                               verbose_name='Количество')

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('-ingredients',)
        constraints = (
            models.UniqueConstraint(
                fields=('ingredients', 'recipe',),
                name='unique_ingredient_amount',
            ),
        )

    def __str__(self):
        return (f"{self.ingredients.name}"
                f"- {self.amount} {self.ingredients.measurement_unit}")


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name="recipes",
                               verbose_name='Автор')
    name = models.CharField(verbose_name='Название рецепта', max_length=300)
    ingredients = models.ManyToManyField(Ingredient,
                                         through=RecipeIngredient,
                                         verbose_name='Ингредиенты',
                                         through_fields=('recipe',
                                                         'ingredients'),)
    tags = models.ManyToManyField('Tag',
                                  through='RecipeTag',
                                  verbose_name='Тэг')
    text = models.TextField(verbose_name='Ваш рецепт',
                            help_text='Опишите ваш рецепт')
    image = models.ImageField(upload_to='receipt/images/',
                              verbose_name='Загрузить фото',
                              help_text='Добавьте изображение'
                              )
    cooking_time = models.PositiveIntegerField(
        validators=[validate_positive],
        verbose_name='Время приготовления'
        )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20,
                            unique=True,
                            verbose_name='Название')
    color = models.CharField(max_length=20,
                             unique=True,
                             verbose_name='Цвет')
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> str:
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50]
        super().save(*args, **kwargs)


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Теги рецепта'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'tag'), name='unique_tag'
            ),
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_user_recipe',
            ),
        )


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        )
