from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.db import models

from .models import Order, OrderItem, Cart, CartItem, Contact
from .serializers import OrderSerializer, CreateOrderSerializer, CartSerializer, ContactSerializer
from catalog.models import Product
from .utils import send_order_confirmation  # Импорт функции отправки email


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Клиенты видят только свои заказы
        return self.queryset.filter(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class CreateOrderView(generics.CreateAPIView):
    serializer_class = CreateOrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartView(APIView):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(id=request.data['product_id'])
        item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = request.data['quantity']
        item.save()
        return Response({'success': True})

    def delete(self, request, pk):
        CartItem.objects.get(id=pk).delete()
        return Response({'success': True})

class ContactView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

class ConfirmOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = user.cart
        contact_id = request.data.get('contact_id')

        if not contact_id:
            return Response({"error": "Contact ID is required"}, status=400)

        try:
            contact = Contact.objects.get(id=contact_id, user=user)
        except Contact.DoesNotExist:
            return Response({"error": "Invalid contact ID"}, status=400)

        # Создание заказа
        order = Order.objects.create(user=user, total_price=cart.items.aggregate(total=models.Sum('product__price'))['total'])

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Очистка корзины после оформления заказа
        cart.items.all().delete()

        # Отправка подтверждения заказа на email
        send_order_confirmation(order)

        return Response(OrderSerializer(order).data, status=201)

class OrderHistoryView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class UpdateOrderStatusView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        order = Order.objects.get(id=pk)
        order.status = request.data.get('status')
        order.save()
        return Response({"success": True, "status": order.status})

