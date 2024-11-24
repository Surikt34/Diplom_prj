from django.core.mail import send_mail
from django.conf import settings
import logging

def send_order_confirmation(order):
    try:
        subject = f"Ваш заказ #{order.id} подтверждён"
        message = (
            f"Здравствуйте, {order.user.first_name}!\n\n"
            f"Ваш заказ успешно оформлен.\n"
            f"Номер заказа: {order.id}\n"
            f"Сумма заказа: {order.total_price}.\n\n"
            "Спасибо за покупку в нашем магазине!"
        )
        recipient_list = [order.user.email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    except Exception as e:
        logging.error(f"Ошибка при отправке email для заказа #{order.id}: {e}")