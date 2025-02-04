import time
import pytest
from django.core.cache import cache
from catalog.models import Product, Category


@pytest.mark.django_db
def test_cachalot_caches_queries(django_assert_num_queries):
    """
    Тест проверяет, что после первого запроса к БД, повторный запрос не делает SQL-запросов
    """
    cache.clear()

    category = Category.objects.create(name="Test Category")
    Product.objects.create(name="Test Product", category=category, price=100, stock=10)

    # Первый запрос (должен сделать 1 SQL-запрос)
    with django_assert_num_queries(1):
        list(Product.objects.all())

    # Второй запрос (должен быть кэширован - 0 SQL-запросов)
    with django_assert_num_queries(0):
        list(Product.objects.all())


@pytest.mark.django_db
def test_cachalot_improves_query_time(capfd):
    """
    Тест проверяет, что второй запрос выполняется быстрее первого благодаря кэшированию.
    """
    cache.clear()

    category = Category.objects.create(name="Test Category")
    Product.objects.create(name="Test Product 2", category=category, price=200, stock=5)

    # Первый запрос (без кэша)
    start = time.perf_counter()
    list(Product.objects.all())
    first_time = time.perf_counter() - start

    # Второй запрос (из кэша)
    start = time.perf_counter()
    list(Product.objects.all())
    second_time = time.perf_counter() - start

    # Вывод результатов
    print(f"⏳ Первый запрос (без кэша): {first_time:.6f} секунд")
    print(f"⚡ Второй запрос (из кэша): {second_time:.6f} секунд")

    # Проверяем, что второй запрос быстрее первого
    assert second_time < first_time, "❌ Кэш не сработал, второй запрос не быстрее первого!"

    # Захватываем вывод теста
    captured = capfd.readouterr()
    print("\n💡 Лог времени выполнения:\n", captured.out)

@pytest.mark.django_db
def test_cachalot_cache_clear(django_assert_num_queries):
    """
    Проверяем, что очистка кэша приводит к повторному SQL-запросу.
    """
    cache.clear()

    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(name="Test Product", category=category, price=100, stock=10)

    # Первый запрос (должен сделать SQL-запрос)
    with django_assert_num_queries(1):
        list(Product.objects.all())

    # Второй запрос (из кэша, без SQL-запроса)
    with django_assert_num_queries(0):
        list(Product.objects.all())

    # Очищаем кэш
    cache.clear()

    # **Обновляем объект перед запросом**, чтобы убедиться, что новый SQL-запрос произошёл
    product.price = 150
    product.save()

    # Запрос (должен снова сделать SQL-запрос, так как объект изменился)
    with django_assert_num_queries(1):
        list(Product.objects.all())