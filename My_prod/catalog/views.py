from rest_framework import generics
from .models import Category, Product, Supplier
from .serializers import CategorySerializer, ProductSerializer, SupplierSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

# Список категорий
class CategoryListView(APIView):
    def get(self, request):
        cached_data = cache.get('category_list')
        if cached_data:
            return Response(cached_data)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        cache.set('category_list', serializer.data, timeout=60 * 15)
        return Response(serializer.data)

# Список товаров
class ProductListView(APIView):
    def get(self, request):
        cached_data = cache.get('product_list')
        if cached_data:
            return Response(cached_data)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        cache.set('product_list', serializer.data, timeout=60 * 15)
        return Response(serializer.data)

# Детали товара
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Список поставщиков
class SupplierListView(APIView):
    def get(self, request):
        cached_data = cache.get('supplier_list')
        if cached_data:
            return Response(cached_data)
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        cache.set('supplier_list', serializer.data, timeout=60 * 15)
        return Response(serializer.data)
