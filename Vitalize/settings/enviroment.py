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
    'CSRF_TRUSTED_ORIGINS', '')
]

ROOT_URLCONF = 'Vitalize.urls'

WSGI_APPLICATION = 'Vitalize.wsgi.application'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
