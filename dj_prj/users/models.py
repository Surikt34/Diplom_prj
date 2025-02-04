from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from versatileimagefield.fields import VersatileImageField

from .enums import UserRoleEnum


class CustomUserManager(BaseUserManager):
    """
    Менеджер для работы с кастомной моделью пользователя.

    Этот менеджер предоставляет методы для создания обычного пользователя
    и суперпользователя, используя email в качестве основного поля для аутентификации.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя с заданным email и паролем.

        :param email: Email пользователя (обязательное поле).
        :param password: Пароль пользователя.
        :param extra_fields: Дополнительные поля модели пользователя.
        :raises ValueError: Если email не предоставлен.
        :return: Созданный экземпляр пользователя.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя с заданным email и паролем.

        Для суперпользователя обязательны параметры is_staff=True и is_superuser=True.
        Если эти параметры не установлены, будет выброшено исключение ValueError.

        :param email: Email суперпользователя (обязательное поле).
        :param password: Пароль суперпользователя.
        :param extra_fields: Дополнительные поля модели суперпользователя.
        :raises ValueError: Если is_staff или is_superuser не равны True.
        :return: Созданный экземпляр суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Кастомная модель пользователя.

    Модель наследуется от AbstractUser и использует email в качестве основного поля для аутентификации.
    Дополнительно содержатся поля для хранения роли пользователя, телефона, адреса, даты рождения,
    статуса верификации, аватара, а также интеграции с Google.
    """
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