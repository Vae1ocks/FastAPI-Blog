from celery import Celery

from .config import settings


celery = Celery("celery", broker=settings.redis.url)
celery.autodiscover_tasks(packages=["src.auth.tasks"])
