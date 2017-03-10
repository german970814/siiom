from django.core.urlresolvers import reverse
from django.utils.functional import SimpleLazyObject

from .models import Empleado


def get_empleado(request):
    if not hasattr(request, '_cache_empleado'):
        try:
            request._cache_empleado = request.user.empleado
        except Empleado.DoesNotExist:
            return None
    return request._cache_empleado


class EmpleadoMiddleWare(object):
    """
    Middleware que se encarga de agregar al empleado al request.
    """

    def process_request(self, request):
        """
        Agrega al request al empleado si el usuario logueado es un empleado.
        """

        if not request.user.is_anonymous() and not request.path.startswith(reverse('admin:index')):
            request.empleado = SimpleLazyObject(lambda: get_empleado(request))
