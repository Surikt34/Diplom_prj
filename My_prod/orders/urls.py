from django.urls import path
from .views import OrderListView, OrderDetailView, CreateOrderView, CartView, ContactView, ConfirmOrderView, \
    OrderHistoryView, UpdateOrderStatusView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('create/', CreateOrderView.as_view(), name='order-create'),
    path('cart/', CartView.as_view(), name='cart'),
    path('contacts/', ContactView.as_view(), name='contact-create'),
    path('confirm/', ConfirmOrderView.as_view(), name='order-confirm'),
    path('history/', OrderHistoryView.as_view(), name='order-history'),
    path('<int:pk>/status/', UpdateOrderStatusView.as_view(), name='order-update-status'),
    path('cart/<int:pk>/', CartView.as_view(), name='cart-delete'),
]