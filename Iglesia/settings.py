# Django settings for Iglesia project.

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@0j2z97_*im(6i-+w5@8gc03l8+2$290k2#bby99-ltjl#m878'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'miembros',
    'academia',
    'grupos',
    # 'googlecharts',
    'reportes',
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
)

ROOT_URLCONF = 'Iglesia.urls'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

#user_server: iglesia
#pass_server: ecbddac9

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
       'NAME': 'iglesia_prod',                      # Or path to database file if using sqlite3.
       'USER': 'german1234',                      # Not used with sqlite3.
       'PASSWORD': '1234',                  # Not used with sqlite3.
       'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
       'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
   }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-CO'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static').replace('\\','/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'#'http://localhost:8000/static/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

AUTH_PROFILE_MODULE = 'miembros.Miembro'

# TEMPLATE_DIRS = (
#     os.path.join(os.path.dirname(__file__), '../Templates').replace('\\','/'),
# )

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR,'templates'),],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
      'django.template.context_processors.debug',
      'django.template.context_processors.request',
      'django.contrib.auth.context_processors.auth',
      'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_PASSWORD = '46ea33cd'
EMAIL_HOST_USER = 'iglesia'