from django.contrib import admin
from django.utils.safestring import mark_safe

from .forms import TagForm
from .models import Favorite, Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag

EMPTY = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'pk')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 2


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'pub_date', 'pk')
    search_fields = ('name', 'author', 'tags')
    list_filter = ('author', 'name', 'tags')
    filter_horizontal = ('tags',)
    empty_value_display = EMPTY
    inlines = (RecipeIngredientInline, RecipeTagInline)
    readonly_fields = ('get_favorites_count',)

    @admin.display(description='Общее число добавлений в избранное')
    def get_favorites_count(self, obj):
        return obj.favorites.count()

    def get_html_photo(self, object):
        return mark_safe(f'<img src="{object.image.url}" width=100>')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', 'pk')
    search_fields = ('name',)
    list_filter = ('name',)
    form = TagForm
    empty_value_display = EMPTY


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'pk', 'ingredients', 'amount')
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = EMPTY


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'recipe',
    )
    search_fields = ('recipe',)
    list_filter = ('recipe', 'user')
    empty_value_display = EMPTY
