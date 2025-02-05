from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailView,
    SupplierListView,
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    path("suppliers/", SupplierListView.as_view(), name="supplier-list"),
]
