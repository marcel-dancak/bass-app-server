import os
import sys

DEBUG = False

ADMINS = [('Marcel', 'dancakm@gmail.com')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRESQL_DB'),
        'USER': os.environ.get('POSTGRESQL_USER'),
        'PASSWORD': os.environ.get('POSTGRESQL_PASSWORD', ''),
        'HOST': os.environ.get('POSTGRESQL_HOST', ''),
        'PORT': os.environ.get('POSTGRESQL_PORT', '5432'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'stdout': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'stream': sys.stdout
        },
        'stderr': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'stream': sys.stderr
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True
        }
    },
    'loggers': {
        'django': {
            'handlers': ['stderr', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True
        },
        'basscloud': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': True
        }
    }
}