"""
Django settings for siiom project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import environ
from .. import database

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 3
env = environ.Env()


# Make this unique, and don't share it with anybody.
SECRET_KEY = '@0j2z97_*im(6i-+w5@8gc03l8+2$290k2#bby99-ltjl#m878'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.localhost']

LOGIN_URL = '/iniciar_sesion/'

# Application definition

SHARED_APPS = [
    'tenant_schemas',

    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',

    'waffle',

    'clientes',  # Maneja las iglesias
]

TENANT_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.contenttypes',

    'waffle',
    'treebeard',

    'pqr',
    'common',
    'grupos',
    'compras',
    'miembros',
    'reportes',
    'encuentros',
    'consolidacion',
    'organizacional',
    'gestion_documental',
    'instituto'
]

INSTALLED_APPS = SHARED_APPS + list(set(TENANT_APPS) - set(SHARED_APPS))

TENANT_MODEL = 'clientes.Iglesia'

MIDDLEWARE_CLASSES = (
    'siiom.middleware.LogNotAllowedHostHeaderMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'tenant_schemas.middleware.TenantMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'miembros.middleware.MiembroMiddleWare',
    'organizacional.middleware.EmpleadoMiddleWare',
)

ROOT_URLCONF = 'siiom.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.media',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'context_processors.siiom_context_processor',
            ],
        },
    },
]

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

SITE_ID = 1

WSGI_APPLICATION = 'siiom.wsgi.application'

# user_server: iglesia
# pass_server: ecbddac9

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASE_ROUTERS = ('tenant_schemas.routers.TenantSyncRouter',)

DATABASES = {
    'default': {
        'ENGINE': 'tenant_schemas.postgresql_backend',
        'NAME': database.NAME,
        'USER': database.USER,
        'PASSWORD': database.PASSWORD,
        'HOST': database.HOST,
        'PORT': database.PORT,
    }
}

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'KEY_FUNCTION': 'tenant_schemas.cache.make_key'
    }
}
# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-CO'

USE_I18N = True

USE_L10N = True

USE_TZ = False

TIME_INPUT_FORMATS = (
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
    '%I:%M %p',     # '06:30 AM'
)

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static').replace('\\','/')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR('../static')
STATICFILES_DIRS = (BASE_DIR('static'),)

# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR('../media')

DEFAULT_FILE_STORAGE = 'siiom.storage.TenantFileSystemStorage'

# Email configuration

DEFAULT_FROM_EMAIL = 'SIIOM <noreply@siiom.net>'

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'tenant_context': {
            '()': 'tenant_schemas.log.TenantContextFilter'
        },
    },
    'formatters': {
        'tenant_context': {
            'format': '[%(schema_name)s:%(domain_url)s] %(levelname)-7s %(asctime)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['tenant_context'],
            'class': 'logging.StreamHandler',
            'formatter': 'tenant_context',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
    },
}

AUTHENTICATION_BACKENDS = (
    'miembros.backends.EmailAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Google analytics
ANALYTICS = env.bool('ANALYTICS', default=False)
