from django.core.management.base import BaseCommand
from versatileimagefield.files import VersatileImageFieldFile
from catalog.models import ProductImage

class Command(BaseCommand):
    help = "Очистка кэша миниатюр VersatileImageField"

    def handle(self, *args, **kwargs):
        images = ProductImage.objects.all()
        cleared_count = 0

        for image in images:
            if isinstance(image.image, VersatileImageFieldFile):
                image.image.delete_all_created_images()  # Удаление всех созданных миниатюр
                cleared_count += 1

        self.stdout.write(f"Кэш миниатюр очищен для {cleared_count} изображений.")