# settings_prod.py
from .settings_common import *

# Override settings for production
DEBUG = False
ALLOWED_HOSTS = ['*']

# Database settings (modify as per your production database)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'osis',
        'USER': 'postgres',
        'PASSWORD': '0',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Add any other production-specific settings here
