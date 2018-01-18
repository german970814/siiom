from .base import *

DEBUG = False

INSTALLED_APPS += ['opbeat.contrib.django']

MIDDLEWARE = ['opbeat.contrib.django.middleware.OpbeatAPMMiddleware'] + MIDDLEWARE

#  Ssl configuration

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Email configuration

EMAIL_HOST_PASSWORD = ENV('EMAIL_HOST_PASSWORD')
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = ENV('EMAIL_HOST_USER')
EMAIL_USE_TLS = True
EMAIL_PORT = '587'

# Logging

LOGGING['handlers']['opbeat'] = {
    'level': 'WARNING',
    'filters': ['tenant_context'],
    'class': 'opbeat.contrib.django.handlers.OpbeatHandler',
    'formatter': 'tenant_context',
}

LOGGING['loggers']['django'] = {
    'level': 'WARNING',
    'handlers': ['opbeat'],
    'propagate': False,
}

# Log errors from the Opbeat module to the console (recommended)
LOGGING['loggers']['opbeat.errors'] = {
    'level': 'ERROR',
    'handlers': ['console'],
    'propagate': False,
}
