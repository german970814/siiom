# Django settings for Iglesia project.

import os
from . import database

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@0j2z97_*im(6i-+w5@8gc03l8+2$290k2#bby99-ltjl#m878'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = '/iniciar_sesion/'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'waffle',
    'treebeard',
    'common',
    'iglesias',
    'miembros',
    'academia',
    'grupos',
    'reportes',
    'encuentros',
    'consolidacion',
    'organizacional',
    'gestion_documental',
    'compras',
    'pqr'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'miembros.middleware.MiembroMiddleWare',
    'organizacional.middleware.EmpleadoMiddleWare',
    'iglesias.middleware.IglesiaMiddleware',
)

ROOT_URLCONF = 'Iglesia.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Iglesia.wsgi.application'

# user_server: iglesia
# pass_server: ecbddac9

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': database.NAME,
        'USER': database.USER,
        'PASSWORD': database.PASSWORD,
        'HOST': database.HOST,
        'PORT': database.PORT,
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

STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Media files

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../media'))

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# ADMIN_MEDIA_PREFIX = '/media/admin/'

# AUTH_PROFILE_MODULE = 'miembros.Miembro'

# Email configuration

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_PASSWORD = '46ea33cd'
EMAIL_HOST_USER = 'iglesia'

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
    },
    'root': {'level': 'INFO'},
}

AUTHENTICATION_BACKENDS = (
    'miembros.backends.EmailAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)
