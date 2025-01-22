from rest_framework import generics
from .models import Category, Product, Supplier
from .serializers import CategorySerializer, ProductSerializer, SupplierSerializer
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

# Список категорий
# class CategoryListView(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

class CategoryListView(APIView):
    def get(self, request):
        cached_data = cache.get('category_list')
        if cached_data:
            return Response(cached_data)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

# Список товаров
# class ProductListView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     filterset_fields = ['category', 'suppliers']
#     search_fields = ['name', 'description']

class ProductListView(APIView):
    def get(self, request):
        cached_data = cache.get('product_list')
        if cached_data:
            return Response(cached_data)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

# Детали товара
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Список поставщиков
# class SupplierListView(generics.ListAPIView):
#     queryset = Supplier.objects.all()
#     serializer_class = SupplierSerializer

class SupplierListView(APIView):
    def get(self, request):
        cached_data = cache.get('supplier_list')
        if cached_data:
            return Response(cached_data)
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data)
