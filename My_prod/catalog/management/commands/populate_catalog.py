from django.core.management.base import BaseCommand
from catalog.models import Category, Product, Supplier

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **kwargs):
        category = Category.objects.create(name="Электроника", description="Раздел электроники")
        supplier = Supplier.objects.create(name="TechSupply", email="info@techsupply.com")

        for i in range(1, 11):
            product = Product.objects.create(
                name=f"Товар {i}",
                category=category,
                price=100 + i * 10,
                stock=50,
                description=f"Описание товара {i}"
            )
            product.suppliers.add(supplier)

        self.stdout.write(self.style.SUCCESS("Каталог успешно заполнен!"))