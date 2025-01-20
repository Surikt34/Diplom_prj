from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_welcome_email(user_email):
    subject = "Добро пожаловать в наш магазин!"
    message = "Спасибо, что зарегистрировались у нас."
    send_mail(subject, message, 'admin@example.com', [user_email])


