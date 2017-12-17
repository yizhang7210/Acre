import os

acre_env = os.environ.get('ACRE_ENV')

if acre_env == 'PROD':
    from .production import *
elif acre_env == 'TEST':
    from .test import *
else:
    from .local import *
