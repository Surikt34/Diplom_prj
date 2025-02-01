from django.db import models
from versatileimagefield.fields import VersatileImageField


class Category(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание категории")
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='subcategories',
        verbose_name="Родительская категория"
    )  # Поддержка древовидной структуры категорий

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255, unique=True, verbose_name="Название поставщика")
    email = models.EmailField(verbose_name="Email поставщика")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон поставщика")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")
    is_active = models.BooleanField(default=True, verbose_name="Активен ли поставщик")

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.name


class Product(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255, verbose_name="Название товара")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категория"
    )
    suppliers = models.ManyToManyField(
        Supplier,
        related_name='products',
        verbose_name="Поставщики"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock = models.PositiveIntegerField(verbose_name="Количество на складе")
    description = models.TextField(blank=True, verbose_name="Описание товара")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attributes',
        verbose_name="Товар"
    )
    name = models.CharField(max_length=255, verbose_name="Название характеристики")
    value = models.CharField(max_length=255, verbose_name="Значение")

    class Meta:
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товаров"

    def __str__(self):
        return f"{self.name}: {self.value}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Товар"
    )
    image = VersatileImageField(
        'Изображение',
        upload_to='catalog/products/',
        placeholder_image='placeholder.jpg'  # изображение по умолчанию
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Описание изображения (alt text)"
    )
    is_main = models.BooleanField(default=False, verbose_name="Главное изображение")

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    def __str__(self):
        return f"Image for {self.product.name}"