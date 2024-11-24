from django.urls import path
from .views import OrderListView, OrderDetailView, CreateOrderView, CartView, ContactView, ConfirmOrderView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('create/', CreateOrderView.as_view(), name='order-create'),
    path('cart/', CartView.as_view(), name='cart'),
    path('contacts/', ContactView.as_view(), name='contact-create'),
    path('confirm/', ConfirmOrderView.as_view(), name='order-confirm'),
]