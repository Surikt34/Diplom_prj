from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def send_order_confirmation_task(order_id):
    """Отправка подтверждения заказа"""
    try:
        order = Order.objects.get(id=order_id)
        subject = f"Подтверждение заказа #{order.id}"
        message = f"Спасибо за ваш заказ!\nСумма заказа: {order.total_price}.\nВаш заказ обрабатывается."
        send_mail(
            subject,
            message,
            "from@example.com",
            [order.user.email],  # Email клиента
            fail_silently=False,
        )
        return f"Подтверждение заказа #{order.id} отправлено."
    except Order.DoesNotExist:
        return f"Заказ с ID {order_id} не найден."


@shared_task
def send_order_status_update_task(order_id, status):
    """Отправка уведомления об обновлении статуса заказа"""
    try:
        order = Order.objects.get(id=order_id)
        subject = f"Обновление статуса заказа #{order.id}"
        message = f"Ваш заказ #{order.id} теперь имеет статус: {status}."
        send_mail(
            subject,
            message,
            "from@example.com",
            [order.user.email],
            fail_silently=False,
        )
        return f"Уведомление об обновлении статуса заказа #{order.id} отправлено."
    except Order.DoesNotExist:
        return f"Заказ с ID {order_id} не найден."


@shared_task
def clear_cart_task(cart_id):
    """
    Очистка корзины после подтверждения заказа.
    """
    from orders.models import Cart

    cart = Cart.objects.get(id=cart_id)
    cart.items.all().delete()
