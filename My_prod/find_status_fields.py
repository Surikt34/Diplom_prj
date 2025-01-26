from django.apps import apps
from django.db import models

def find_status_fields():
    for model in apps.get_models():
        for field in model._meta.fields:
            if field.name == "status" and hasattr(field, "choices"):
                print(f"Модель: {model.__name__}, поле: {field.name}, path: {model.__module__}.{model.__name__}")

find_status_fields()