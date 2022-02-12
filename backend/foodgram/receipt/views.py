from django.db.models import Sum
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeReadSerializer, RecipeSerializer,
                             ShoppingListSerializer, TagSerializer)
from foodgram.pagination import LimitPageNumberPagination
from foodgram.permissions import IsAuthorOrAdminOrReadOnly
from receipt.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)

from .filters import RecipeFilter


class ListRetrieveViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class ListCreatDeleteViewSet(mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    pass


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    permission_classes = (IsAuthorOrAdminOrReadOnly, )
    filterset_class = RecipeFilter
    filter_backends = (DjangoFilterBackend,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeSerializer

    @staticmethod
    def post_method_for_action(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if 'shopping_cart' in request.path:
            try:
                serializer.save()
            except IntegrityError:
                return Response('Рецепт уже в списке покупок')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif 'favorite' in request.path:
            try:
                serializer.save()
            except IntegrityError:
                return Response('Рецепт уже в избранном')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_for_action(request=request, pk=pk,
                                           serializers=FavoriteSerializer)

    @action(methods=['POST'], detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_method_for_action(request=request, pk=pk,
                                           serializers=ShoppingListSerializer)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_object = model.objects.filter(user=user, recipe=recipe)
        if model_object.exists():
            model_object.delete()
            if 'shopping_cart' in request.path:
                return Response('Рецепт удалён из списка покупок',
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response('Рецепт удалён из избранного',
                                status=status.HTTP_204_NO_CONTENT)
        else:
            if 'shopping_cart' in request.path:
                return Response('Рецепт уже удалён из списка покупок',
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Рецепт уже удалён из избранного',
                                status=status.HTTP_400_BAD_REQUEST)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingList
        )

    @action(detail=False, permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredients__name',
            'ingredients__measurement_unit').annotate(total=Sum('amount'))
        shopping_list = 'Cписок покупок:\n'
        if ingredients:
            for number, ingredient in enumerate(ingredients, start=1):
                shopping_list += (
                    f'{number} '
                    f'{ingredient["ingredients__name"]} - '
                    f'{ingredient["total"]} '
                    f'{ingredient["ingredients__measurement_unit"]}\n')

            purchase_list = 'purchase_list.txt'
            response = HttpResponse(shopping_list,
                                    content_type='text/plain')
            response['Content-Disposition'] = (f'attachment;'
                                               f'filename={purchase_list}')
            return response
        return HttpResponse('Список пуст')


class FavoriteViewSet(ListCreatDeleteViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class GetIngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name']
    permission_classes = (permissions.AllowAny,)


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
