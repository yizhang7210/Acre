from celery.schedules import crontab

from .base import *

# Local configs
SECRET_KEY = env('DJANGO_SECRET_KEY', default='kh+n-p+wicf&in532@&w9^8b*l)^5#_$ym%cch8nlgv8*ri_!2')
DEBUG = env.bool('DJANGO_DEBUG', default=True)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'acre',
        'USER': 'acreuser',
        'PASSWORD': 'acrelocaldb',
        'HOST': 'localhost',
    }
}

# Celery related
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_BEAT_SCHEDULE = {
    'daily-update': {
        'task': 'algos.main.main',
        'schedule': crontab(minute=0, hour=17)
    },
}
