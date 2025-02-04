from __future__ import absolute_import, unicode_literals

# Celery всегда импортируется, когда запускается Django
from dj_prj.My_prod.celery import app as celery_app

__all__ = ('celery_app',)