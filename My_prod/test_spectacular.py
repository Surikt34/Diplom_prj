import os
import django
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.settings import spectacular_settings

# Установить переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'My_prod.settings')

# Настроить Django
django.setup()

# Проверить настройки ENUM_NAME_OVERRIDES
print("ENUM_NAME_OVERRIDES:", spectacular_settings.ENUM_NAME_OVERRIDES)

# Проверить доступность UserRoleEnum
from users.models import UserRoleEnum
print("UserRoleEnum:", UserRoleEnum)
print("Choices:", UserRoleEnum.choices())

# Сгенерировать схему
generator = SchemaGenerator()
schema = generator.get_schema(request=None, public=True)
print(schema)