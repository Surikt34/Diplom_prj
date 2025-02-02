from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.signals import task_failure
import rollbar

# Установка настроек Django для Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'My_prod.settings')

app = Celery('My_prod')

# настройки Django как основу для конфигурации Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач в приложениях Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Автоматический мониторинг ошибок Celery
@task_failure.connect
def handle_task_failure(sender, task_id, args, kwargs, einfo, **other_kwargs):
    rollbar.report_exc_info(extra_data={'task_id': task_id})