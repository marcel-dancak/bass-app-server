"""
Django settings for BassCloud
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


### DEBUG
DEBUG = True


### DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bass',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}

### SECRET KEY
SECRET_KEY = '{{ secret_key }}'


### INTERNATIONALIZATION
LANGUAGES = (
    ('en-us', 'English'),
)
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Bratislava'
USE_I18N = True
USE_L10N = True
USE_TZ = True


### OTHER
ALLOWED_HOSTS = ['*']

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media/')


### SYSTEM CONFIGURATION
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211'
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders':[
                ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    }
]

# enable CORS requests
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = (
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'basscloud.accounts',
    'basscloud.catalog',
    'basscloud.app',
    'basscloud.feedback',
    'basscloud.seo'
)

ROOT_URLCONF = '{{ project_name }}.urls'
WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

AUTH_USER_MODEL = 'catalog.User'


# Accounts Registration
ACCOUNT_SITE_NAME = 'BassCloud'
ACCOUNT_ACTIVATION_DAYS = 3
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587


### CUSTOM SETTINGS
try:
    from {{ project_name }}.settings_custom import *
except ImportError:
    pass


### ENVIRONMENT VARIABLES SETTINGS
for k, v in os.environ.items():
    if k.startswith("DJANGO_"):
        if v:
            if v[0] in ("'", '"'):
                v = v[1:-1]
            else:
                try:
                    if v in ('True', 'False'):
                        v = True if v == 'True' else False
                    elif '.' in v:
                        v = float(v)
                    else:
                        v = int(v)
                except ValueError:
                    # let it be a string
                    if k != 'DJANGO_SETTINGS_MODULE':
                        logger.warn('Warning: {0} - Invalid number value, converting to string'.format(k))
        key = k.split('_', 1)[1]
        globals()[key] = v


# vim: set ts=8 sts=4 sw=4 et:
