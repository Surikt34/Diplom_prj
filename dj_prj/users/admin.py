from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительные поля",
            {
                "fields": (
                    "role",
                    "phone",
                    "address",
                    "date_of_birth",
                    "avatar",
                    "is_verified",
                ),
            },
        ),
    )
    list_display = ["username", "email", "role", "is_verified", "avatar_thumbnail"]

    def avatar_thumbnail(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px;" />',
                obj.avatar.thumbnail["50x50"].url,
            )
        return "No avatar"

    avatar_thumbnail.short_description = "Avatar"
    list_filter = ["role", "is_verified"]
