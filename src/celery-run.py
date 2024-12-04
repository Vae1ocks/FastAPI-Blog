import sys

from infrastructure.celery import celery_app

if __name__ == "__main__":
    sys.argv.append('worker')
    celery_app.start(argv=sys.argv[1:])
