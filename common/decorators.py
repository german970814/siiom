# Django imports
from django.contrib.auth.decorators import user_passes_test  # , login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

# Locale imports
from . import constants

# Python imports
from functools import wraps
from threading import Thread
import json


def permisos_requeridos(*permisos):
    """
    Decorador para vistas que chequea si el usuario tiene algún permiso habilitado. Si no tiene ningún permiso se
    levanta la excepción PermissionDenied.
    """

    def chequear_permisos(user):
        for permiso in permisos:
            if user.has_perm(permiso):
                return True

        raise PermissionDenied

    return user_passes_test(chequear_permisos)


def login_required_api(view_func):
    """Decorador para saber si un usuario está logeado o no en una API, retornando una respuesta JSON."""

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        return HttpResponse(
            json.dumps({
                constants.RESPONSE_CODE: constants.RESPONSE_DENIED,
                'message': 'User not authenticated'
            }),
            content_type=constants.CONTENT_TYPE_API
        )
    return wrapped_view


def concurrente(function):
    """
    Funcion para manejar concurrencia.

    :returns:
        Un hilo con la ejecución de la funcion asignada.
    """

    @wraps(function)
    def decorator(*args, **kwargs):
        hilo = Thread(target=function, args=args, kwargs=kwargs)
        hilo.daemon = True
        hilo.start()
        return hilo
    return decorator
