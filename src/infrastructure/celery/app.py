from celery import Celery

from .config import celery_config


celery = Celery("celery", broker=celery_config.redis.url)
celery.autodiscover_tasks(packages=["src.infrastructure.celery.tasks"])
