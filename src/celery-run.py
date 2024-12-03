import sys

from infrastructure.celery.app import celery

if __name__ == "__main__":
    sys.argv.append('worker')
    celery.start(argv=sys.argv[1:])
