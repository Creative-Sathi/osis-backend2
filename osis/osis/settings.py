# settings.py
import os
from decouple import config, Csv

# Detect the environment
environment = os.environ.get('DJANGO_ENV', config('DJANGO_ENV', default='development'))  # development, deployment or production

# Load common settings
from .settings_common import *

# Load environment-specific settings
if environment == 'production':
    from .settings_prod import *
elif environment == 'deployment':
    from .settings_deploy import *
else:
    from .settings_dev import *
