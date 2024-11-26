from celery import Celery

from .config import celery_settings


celery = Celery("celery", broker=celery_settings.redis.url)
celery.autodiscover_tasks(packages=["src.infrastructure.celery.tasks"])
