"""
Django settings for brickfiesta project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import json
import os

from django.core.exceptions import ImproperlyConfigured

with open("settings.json") as f:
    settings_keys = json.loads(f.read())


def get_variable(str_var_name, settings=settings_keys):
    """ Get the environment variable needed for by the system. """
    try:
        return settings[str_var_name]
    except KeyError:
        str_error_msg = "Set the {} environment variable.".format(str_var_name)
        raise ImproperlyConfigured(str_error_msg)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.join(os.path.abspath(__file__))))

SECRET_KEY = get_variable("SECRET_KEY")
GOOGLE_RECAPTCHA_KEY = get_variable("GOOGLE_RECAPTCHA_KEY")
GOOGLE_RECAPTCHA_SITE_KEY = get_variable("GOOGLE_RECAPTCHA_SITE_KEY")
GOOGLE_MAP_KEY = get_variable("GOOGLE_MAP_KEY")
SQUARE_CART_KEY = get_variable("SQUARE_CART_KEY")
SQUARE_LOCATION_KEY = get_variable("SQUARE_LOCATION_KEY")

LOGIN_REDIRECT_URL = '/afol/profile/'
LOGIN_URL = '/afol/login/'
DEFAULT_FROM_EMAIL = 'customer.support@brickfiesta.com'
SITE_ID = 1
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CART_SESSION_ID = 'cart'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'afol.apps.AfolConfig',
    'event.apps.EventConfig',
    'donations.apps.DonationsConfig',
    'games.apps.GamesConfig',
    'mocs.apps.MocsConfig',
    'news.apps.NewsConfig',
    'planning.apps.PlanningConfig',
    'referral.apps.ReferralConfig',
    'shop.apps.ShopConfig',
    'vendor.apps.VendorConfig',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'qr_code',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    # 'shop.cart_middleware.InitializeCart',
]

ROOT_URLCONF = 'brickfiesta.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.cart_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'brickfiesta.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/static/media/'
MEDIA_ROOT = os.path.join(os.path.join(BASE_DIR, 'static'), 'media')
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "static"),
]
