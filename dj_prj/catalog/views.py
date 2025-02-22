import rollbar
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Product, Supplier
from .serializers import CategorySerializer, ProductSerializer, SupplierSerializer


class CategoryListView(generics.ListAPIView):
    """
    Представление для получения списка категорий.

    Кэширует результаты на 15 минут для оптимизации запросов.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        """
        Получить список категорий.
        Проверяет кэш перед выполнением запроса.
        """
        cached_data = cache.get("category_list")
        if cached_data:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        cache.set("category_list", response.data, timeout=60 * 15)
        return response


class ProductListView(generics.ListAPIView):
    """
    Представление для получения списка товаров.

    Поддерживает фильтрацию по категориям и поставщикам,
    а также поиск по названию и описанию.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ["category", "suppliers"]
    search_fields = ["name", "description"]

    def list(self, request, *args, **kwargs):
        """
        Получить список товаров.
        Проверяет кэш перед выполнением запроса.
        """
        cached_data = cache.get("product_list")
        if cached_data:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        cache.set("product_list", response.data, timeout=60 * 15)
        return response


class ProductDetailView(generics.RetrieveAPIView):
    """
    Представление для получения информации о конкретном товаре.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SupplierListView(generics.ListAPIView):
    """
    Представление для получения списка поставщиков.

    Кэширует результаты на 15 минут для оптимизации запросов.
    """

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def list(self, request, *args, **kwargs):
        """
        Получить список поставщиков.
        Проверяет кэш перед выполнением запроса.
        """
        cached_data = cache.get("supplier_list")
        if cached_data:
            return Response(cached_data)
        response = super().list(request, *args, **kwargs)
        cache.set("supplier_list", response.data, timeout=60 * 15)
        return response


class RollbarTestAPIView(APIView):
    """
    APIView, которая вызывает исключение для тестирования интеграции с Rollbar.
    """

    permission_classes = []  # ОТКЛЮЧАЕМ ТРЕБОВАНИЕ АВТОРИЗАЦИИ

    def get(self, request, *args, **kwargs):
        try:
            1 / 0  # Намеренно вызываем ошибку
        except ZeroDivisionError:
            rollbar.report_exc_info()  # Отправляем ошибку в Rollbar
            return Response(
                {"error": "Что-то пошло не так!"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"message": "Все в порядке!"}, status=status.HTTP_200_OK)
