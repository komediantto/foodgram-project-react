from django.urls import include, path
from receipt.views import GetIngredientViewSet, RecipeViewSet, TagViewSet
from rest_framework.routers import DefaultRouter

r1 = DefaultRouter()
r1.register('ingredients', GetIngredientViewSet)
r1.register('recipes', RecipeViewSet, basename='recipes')
r1.register('tags', TagViewSet)

urlpatterns = [
    path('', include(r1.urls)),
]
