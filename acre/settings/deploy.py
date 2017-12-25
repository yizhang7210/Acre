from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'circle_test',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'circleci',
        'PASSWORD': '',
    }
}
