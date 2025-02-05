import yaml
from django.core.management.base import BaseCommand
from catalog.models import Product, Category, Supplier, ProductAttribute


class Command(BaseCommand):
    help = "Импорт товаров от поставщика из YAML-файла"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к YAML-файлу для импорта")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]

        try:
            # Открываем и читаем YAML-файл
            with open(file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)

            # Создаём или находим поставщика
            shop_name = data.get("shop")
            supplier, created = Supplier.objects.get_or_create(name=shop_name)

            if created:
                self.stdout.write(f"Поставщик '{shop_name}' добавлен.")
            else:
                self.stdout.write(f"Поставщик '{shop_name}' найден.")

            # Обработка категорий
            category_mapping = {}
            for category_data in data.get("categories", []):
                category, _ = Category.objects.get_or_create(
                    id=category_data["id"], defaults={"name": category_data["name"]}
                )
                category_mapping[category_data["id"]] = category
                self.stdout.write(f"Категория '{category.name}' обработана.")

            # Обработка товаров
            for product_data in data.get("goods", []):
                category_id = product_data["category"]
                category = category_mapping.get(category_id)

                if not category:
                    self.stdout.write(
                        f"Категория с ID {category_id} не найдена. Пропуск товара."
                    )
                    continue

                product, created = Product.objects.update_or_create(
                    id=product_data["id"],
                    defaults={
                        "name": product_data["name"],
                        "description": product_data["model"],
                        "category": category,
                        "price": product_data["price"],
                        "stock": product_data["quantity"],
                    },
                )
                product.suppliers.add(supplier)

                # Обработка характеристик
                for attr_name, attr_value in product_data.get("parameters", {}).items():
                    ProductAttribute.objects.update_or_create(
                        product=product, name=attr_name, defaults={"value": attr_value}
                    )

                if created:
                    self.stdout.write(f"Товар '{product.name}' добавлен.")
                else:
                    self.stdout.write(f"Товар '{product.name}' обновлён.")

        except FileNotFoundError:
            self.stderr.write(f"Файл '{file_path}' не найден.")
        except yaml.YAMLError as e:
            self.stderr.write(f"Ошибка чтения YAML-файла: {e}")
