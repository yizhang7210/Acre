import os

acre_env = os.environ.get('ACRE_ENV')

if acre_env == 'PROD':
    from .production import *
elif acre_env == 'DEV':
    from .dev import *
elif acre_env == 'DEPLOY':
    from .deploy import *
else:
    from .local import *
