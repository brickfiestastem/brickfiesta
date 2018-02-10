import os

SECRET_KEY = ''
GOOGLE_MAP_KEY = ''
SQUARE_CART_KEY = ''
SQUARE_LOCATION_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join('.', 'db.sqlite3'),
    }
}
