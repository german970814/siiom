from .base import *

MIDDLEWARE_CLASSES = (
    'siiom.middleware.LogNotAllowedHostHeaderMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'tenant_schemas.middleware.TenantMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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

#  Apps
SHARED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

INSTALLED_APPS = SHARED_APPS + list(set(TENANT_APPS) - set(SHARED_APPS))

#  Debug toolbar
INTERNAL_IPS = ['127.0.0.1']
