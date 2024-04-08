# settings_dev.py
from .settings_common import *

# Override settings for development
DEBUG = True
ALLOWED_HOSTS = ['*']

# Database settings for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'osis',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_postgres.core.PostgresChannelLayer',
        'CONFIG': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'osis',
            'USER': 'postgres',
            'PASSWORD': 'root',
            'HOST': '127.0.0.1',
            'PORT': '5432',

          
            }
        },
}


# Add any other development-specific settings here
