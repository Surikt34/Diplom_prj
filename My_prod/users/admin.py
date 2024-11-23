from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные поля', {
            'fields': ('role', 'phone', 'address', 'date_of_birth', 'avatar', 'is_verified'),
        }),
    )
    list_display = ['username', 'email', 'role', 'is_verified']
    list_filter = ['role', 'is_verified']