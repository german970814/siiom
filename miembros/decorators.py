from common.decorators import permisos_requeridos
from django.core.exceptions import PermissionDenied

from functools import wraps


def miembro_property_test_decorator(view_func, property='es_cabeza_red', function=lambda x: x):
    """
    Decorador para usuarios miembros, la cual verifica un property de el modelo del miembro,
    y evalua una funcion como prueba, de no cumplir la prueba, verifica si es administrador, o de
    lo contrario, levanta una excepcion.

    :returns:
        view_func, la funcion o vista a la cual se está asignando el decorador.

    :param: property
        La propiedad de el objeto de miembro que será evaluada, lo recomendable es usar una propiedad
        que retorne `True` o `False` para ser evaluada como `bool`.

    :param: function
        Una función la cual es evaluada al momento de verificar la propiedad de el miembro,
        con el fin de hacer una prueba mas completa y exacta.
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if hasattr(request, 'miembro'):
            if function(getattr(request.miembro, property)):
                return view_func(request, *args, **kwargs)
            else:
                return \
                    permisos_requeridos('miembros.es_administrador')(view_func)(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrapped_view


def user_is_director_red(view_func):
    """
    Decorador para usuarios que son directores de red o administradores, en caso no pertenecer a
    ningún grupo, levanta una exception de PermissionDenied con código http 403.

    :returns: view_func, la funcion de vista a la que fue asignado el decorador.
    """

    return miembro_property_test_decorator(view_func, property='es_director_red')


def user_is_cabeza_red(view_func):
    """
    Decorador para usuarios que son cabeza de red o administradores, en caso de no pertenecer a ningún
    area, levanta una excepcion de PermissionDenied con código http 403.

    :returns: view_func, la funcion de vista a la que fue asignado el decorador.
    """

    return miembro_property_test_decorator(view_func)
