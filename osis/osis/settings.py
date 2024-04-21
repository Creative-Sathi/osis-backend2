# settings.py
import os

# Detect the environment
environment = 'development'  # development, deployment or production

# Load common settings
from .settings_common import *

# Load environment-specific settings
if environment == 'production':
    from .settings_prod import *
elif environment == 'deployment':
    from .settings_deploy import *
else:
    from .settings_dev import *
