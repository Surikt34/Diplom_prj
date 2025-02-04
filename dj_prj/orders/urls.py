from django.urls import path
from .views import OrderListView, OrderDetailView, CreateOrderView, ContactView, ConfirmOrderView, \
    OrderHistoryView, UpdateOrderStatusView, GetCartView, AddToCartView, RemoveFromCartView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('create/', CreateOrderView.as_view(), name='order-create'),
    path('cart/', GetCartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/<int:pk>/', RemoveFromCartView.as_view(), name='cart-delete'),
    path('contacts/', ContactView.as_view(), name='contact-create'),
    path('confirm/', ConfirmOrderView.as_view(), name='order-confirm'),
    path('history/', OrderHistoryView.as_view(), name='order-history'),
    path('<int:pk>/status/', UpdateOrderStatusView.as_view(), name='order-update-status'),

]