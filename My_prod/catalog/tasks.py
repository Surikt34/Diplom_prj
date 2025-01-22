from celery import shared_task
from django.core.cache import cache
from .models import Category, Product, Supplier
from .serializers import CategorySerializer, ProductSerializer, SupplierSerializer


@shared_task
def cache_categories():
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    cache.set('category_list', serializer.data, timeout=3600)  # Кэш на 1 час


@shared_task
def cache_products():
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    cache.set('product_list', serializer.data, timeout=3600)  # Кэш на 1 час


@shared_task
def cache_suppliers():
    suppliers = Supplier.objects.all()
    serializer = SupplierSerializer(suppliers, many=True)
    cache.set('supplier_list', serializer.data, timeout=3600)  # Кэш на 1 час