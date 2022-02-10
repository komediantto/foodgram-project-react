from django.contrib import admin
from django.utils.safestring import mark_safe

from .forms import TagForm
from .models import Favorite, Ingredient, Recipe, RecipeIngredient, Tag

# Register your models here.
EMPTY = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "text", "time", "pub_date", 'pk')
    search_fields = ("title", "author")
    empty_value_display = EMPTY
    save_on_top = True

    def get_html_photo(self, object):
        return mark_safe(f"<img src='{object.image.url}' width=100>")


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'pk')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', 'pk')
    search_fields = ('name',)
    list_filter = ('name',)
    form = TagForm
    empty_value_display = EMPTY


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', "pk", "ingredient", "amount")
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
