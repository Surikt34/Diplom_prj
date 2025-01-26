from rest_framework import serializers
from .models import Order, OrderItem, CartItem, Cart, Contact
from catalog.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для элементов заказа.
    """
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заказа.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'total_price', 'items']


class CreateOrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания заказа.
    """
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


class CartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для элементов корзины.
    """
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для корзины пользователя.
    """
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items']


class ContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор для контактной информации пользователя.
    """
    class Meta:
        model = Contact
        fields = '__all__'


class UpdateOrderStatusSerializer(serializers.Serializer):
    """
    для обработки статуса заказа.
    """
    status = serializers.ChoiceField(choices=['pending', 'completed', 'canceled'])


class CartItemCreateSerializer(serializers.Serializer):
    """
    для обработки данных при добавлении товаров в корзину.
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class ConfirmOrderSerializer(serializers.Serializer):
    """
    сериализатор для подтверждения заказа
    """
    contact_id = serializers.IntegerField()


