from django.contrib import admin
from .models import Category, Product, Supplier, ProductAttribute, ProductImage
from django.contrib.admin import SimpleListFilter  #  базовый фильтр

# Кастомный фильтр для поиска по названию
class NameFilter(SimpleListFilter):
    title = 'Название'
    parameter_name = 'name'

    def lookups(self, request, model_admin):
        return [(p.name, p.name) for p in Product.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(name__icontains=self.value())
        return queryset

# Инлайн для ProductImage
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    classes = ('collapse',)

# Инлайн для ProductAttribute
class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    classes = ('collapse',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'updated_at')
    list_filter = ('category', NameFilter)  # Исправленный фильтр
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ProductAttributeInline]

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active')
    search_fields = ('name', 'email')

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value')
    list_filter = ('name',)

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_main')