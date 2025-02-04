from rest_framework import generics, status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import UserRateThrottle, SimpleRateThrottle
from rest_framework.views import APIView
from django.db import models
from .models import Order, OrderItem, Cart, CartItem, Contact
from .serializers import OrderSerializer, CreateOrderSerializer, CartSerializer, ContactSerializer, \
    UpdateOrderStatusSerializer, ConfirmOrderSerializer, CartItemCreateSerializer, CartItemSerializer
from catalog.models import Product
from .utils import send_order_confirmation
from .tasks import send_order_confirmation_task, send_order_status_update_task, send_order_confirmation_task, clear_cart_task
from drf_spectacular.utils import extend_schema

class BurstRateThrottle(SimpleRateThrottle):
    scope = 'burst'

    def get_cache_key(self, request, view):
        return self.get_ident(request)  # Ограничение по IP

class OrderListView(generics.ListAPIView):
    """
     Отображение для получения списка заказов пользователя.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Клиенты видят только свои заказы
        return self.queryset.filter(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    """
    Отображение для получения детальной информации о заказе.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class CreateOrderView(generics.CreateAPIView):
    """
    Отображение для создания нового заказа.
    """
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GetCartView(GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(operation_id="get_cart_content")
    def get(self, request):
        """
        Получить содержимое корзины.
        """
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = self.serializer_class(cart)
        return Response(serializer.data)

class AddToCartView(GenericAPIView):
    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(operation_id="add_to_cart")
    def post(self, request):
        """
        Добавить товар в корзину или обновить его количество.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            cart, _ = Cart.objects.get_or_create(user=request.user)
            product = Product.objects.get(id=serializer.validated_data['product_id'])
            quantity = serializer.validated_data['quantity']

            item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                item.quantity += quantity
            else:
                item.quantity = quantity
            item.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveFromCartView(GenericAPIView):
    """
    Отображение для удаления товара из корзины.
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(operation_id="remove_from_cart")
    def delete(self, request, pk):
        """
        Удалить товар из корзины.
        """
        CartItem.objects.get(id=pk).delete()
        return Response({'success': True}, status=status.HTTP_200_OK)

class ContactView(APIView):
    """
    Отображение для управления контактной информацией пользователя.
    """
    serializer_class = ContactSerializer

    def post(self, request):
        """
        Создать новую контактную информацию.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmOrderView(APIView):
    """
    Отображение для подтверждения заказа и очистки корзины.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ConfirmOrderSerializer

    def post(self, request):
        """
        Подтвердить заказ и отправить email-подтверждение.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.user
            cart = user.cart
            contact_id = serializer.validated_data['contact_id']

            try:
                contact = Contact.objects.get(id=contact_id, user=user)
            except Contact.DoesNotExist:
                return Response({"error": "Invalid contact ID"}, status=400)

            order = Order.objects.create(
                user=user,
                total_price=cart.items.aggregate(total=models.Sum('product__price'))['total']
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            clear_cart_task.delay(cart.id)
            send_order_confirmation_task.delay(order.id)

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderHistoryView(ListAPIView):
    """
    Отображение для получения истории заказов пользователя.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class UpdateOrderStatusView(APIView):
    """
    Отображение для обновления статуса заказа (только для администратора).
    """
    permission_classes = [IsAdminUser]
    serializer_class = UpdateOrderStatusSerializer

    def patch(self, request, pk):
        """
        Обновить статус конкретного заказа.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order = Order.objects.get(id=pk)
            order.status = serializer.validated_data['status']
            order.save()
            send_order_status_update_task.delay(order.id, order.status)
            return Response({"success": True, "status": order.status}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)