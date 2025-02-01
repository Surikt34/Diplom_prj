from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from versatileimagefield.fields import VersatileImageField

from .enums import UserRoleEnum


class CustomUserManager(BaseUserManager):
    # Метод для создания пользователя
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Метод для создания суперпользователя
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRoleEnum.choices(),
        default=UserRoleEnum.CLIENT.value,
        verbose_name="Роль"
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Телефон",
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Введите корректный номер телефона")]
    )
    address = models.TextField(blank=True, null=True, verbose_name="Адрес")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Дата рождения")
    is_verified = models.BooleanField(default=False, verbose_name="Пользователь верифицирован")
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = VersatileImageField(
        'Аватар',
        upload_to='avatars/',
        blank=True,
        null=True
    )

    # для интеграции с Google
    google_id = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="Google ID")
    google_profile_picture = models.URLField(blank=True, null=True, verbose_name="Фото профиля Google")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"