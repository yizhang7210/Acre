from .base import *

# Local configs
SECRET_KEY = env('DJANGO_SECRET_KEY', default='kh+n-p+wicf&in532@&w9^8b*l)^5#_$ym%cch8nlgv8*ri_!2')
DEBUG = env.bool('DJANGO_DEBUG', default=True)
