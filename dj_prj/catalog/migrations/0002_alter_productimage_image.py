# Generated by Django 5.1.3 on 2025-02-01 12:34

import versatileimagefield.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productimage",
            name="image",
            field=versatileimagefield.fields.VersatileImageField(
                upload_to="products/images/", verbose_name="Изображение"
            ),
        ),
    ]
