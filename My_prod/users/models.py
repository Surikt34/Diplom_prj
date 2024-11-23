from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('supplier', 'Supplier'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client', verbose_name="Роль")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Телефон")
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    is_verified = models.BooleanField(default=False, verbose_name="Пользователь верифицирован")

    def __str__(self):
        return f"{self.username} ({self.role})"
