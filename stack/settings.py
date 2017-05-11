"""
Django settings for stack project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import certifi
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6q3dr8ffl^d79npzgr6wg!r$oe^a(au_o=&31v^orh&t)e=dp!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False) == 'True'

TEMPLATE_DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth'
            ],
        },
    },
]

ALLOWED_HOSTS = [host for host in os.environ['ALLOWED_HOSTS'].split(",")]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'qa'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'stack.urls'

WSGI_APPLICATION = 'stack.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


if os.path.isfile('/run/secrets/elastic_cloud_auth'):
    with open('/run/secrets/elastic_cloud_auth', 'r') as f:
        ES_AUTH = f.read().strip()
else:
    ES_AUTH = ""

ES_HOST = os.environ.get('ES_HOST', 'http://localhost:9200')

ES_INDEX = os.environ.get('ES_INDEX', 'stack')
ES_INDEX_SETTINGS = {
    'number_of_shards': 1,
    'number_of_replicas': 0,
}

ES_CONNECTIONS = {
    'default': {
        'hosts': [{
            'host': ES_HOST,
            'http_auth': ES_AUTH,
            'verify_certs': False,
            'use_ssl': os.environ.get('ES_USE_SSL', False) == 'True',
            'port': os.environ.get('ES_PORT', '9200'),
        }]
    }
}

