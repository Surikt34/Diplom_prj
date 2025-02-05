# Generated by Django 5.1.3 on 2025-01-27 17:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="role",
            field=models.CharField(
                choices=[
                    ("client", "CLIENT"),
                    ("supplier", "SUPPLIER"),
                    ("admin", "ADMIN"),
                ],
                default="client",
                max_length=20,
                verbose_name="Роль",
            ),
        ),
    ]
