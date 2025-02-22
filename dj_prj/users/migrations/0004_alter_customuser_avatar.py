# Generated by Django 5.1.3 on 2025-02-01 12:34

import versatileimagefield.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_customuser_google_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="avatar",
            field=versatileimagefield.fields.VersatileImageField(
                blank=True, null=True, upload_to="avatars/", verbose_name="Аватар"
            ),
        ),
    ]
