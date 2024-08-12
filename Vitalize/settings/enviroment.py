from os import environ
from pathlib import Path
from typing import List

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ.get('SECRET_KEY', 'INSECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if environ.get('DEBUG') == '0' else True

ALLOWED_HOSTS: List = [environ.get(
    'ALLOWED_HOSTS', '127.0.0.1'
)]

CSRF_TRUSTED_ORIGINS: List = [environ.get(
<<<<<<< HEAD
    'CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1')
=======
    'CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1:8000')
>>>>>>> 4a34220c166bd51318cf05340fa42401ff677862
]

ROOT_URLCONF = 'Vitalize.urls'

WSGI_APPLICATION = 'Vitalize.wsgi.application'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
