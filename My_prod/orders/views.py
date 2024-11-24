from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Order, OrderItem, Cart, CartItem, Contact
from .serializers import OrderSerializer, CreateOrderSerializer, CartSerializer, ContactSerializer
from catalog.models import Product


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
    def post(self, request):
        cart = request.user.cart
        contact = Contact.objects.get(id=request.data['contact_id'])
        order = Order.objects.create(user=request.user, total_price=cart.total_price)
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        cart.items.all().delete()
        return Response(OrderSerializer(order).data)

class OrderHistoryView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

