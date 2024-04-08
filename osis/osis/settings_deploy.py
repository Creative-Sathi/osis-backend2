# settings_deploy.py
from .settings_common import *

# Override settings for deployment
DEBUG = False
ALLOWED_HOSTS = ['yourdeploymentdomain.com']

# Database settings (modify as per your deployment database)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_deploy_db_name',
        'USER': 'your_deploy_db_user',
        'PASSWORD': 'your_deploy_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Add any other deployment-specific settings here
