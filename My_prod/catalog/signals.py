from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Category, Product, Supplier
from .tasks import cache_categories, cache_products, cache_suppliers


@receiver([post_save, post_delete], sender=Category)
def update_category_cache(sender, **kwargs):
    cache_categories.delay()


@receiver([post_save, post_delete], sender=Product)
def update_product_cache(sender, **kwargs):
    cache_products.delay()


@receiver([post_save, post_delete], sender=Supplier)
def update_supplier_cache(sender, **kwargs):
    cache_suppliers.delay()