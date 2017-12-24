from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'acre-dev',
        'HOST': 'acre-dev.cogg3eyv8mdl.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
        'USERNAME': 'acredev',
        'PASSWORD': 'acre-dev',
    }
}
