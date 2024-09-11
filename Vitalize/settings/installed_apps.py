INSTALLED_APPS = [
    'Users',
    'Products',
    'Sales',
    'Schedules',
    'CashRegister',
    'Logs',
    # jazzmin
    'jazzmin',
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # crispy forms
    'crispy_forms',
    'crispy_bootstrap5',
    # all auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # cors headers
    'corsheaders',
    # debug toolbar
    'debug_toolbar',
    # axes
    'axes',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'
