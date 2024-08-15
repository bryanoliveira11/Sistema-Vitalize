AUTHENTICATION_BACKENDS = [
    # AxesStandaloneBackend should be the first backend in the
    # AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesStandaloneBackend',
    # all auth
    'allauth.account.auth_backends.AuthenticationBackend',
    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'Users.VitalizeUser'
