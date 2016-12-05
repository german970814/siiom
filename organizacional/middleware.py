from django.core.urlresolvers import reverse
from .models import Empleado


class EmpleadoMiddleWare(object):
    """
    Middleware que se encarga de agregar al empleado al request.
    """

    def process_request(self, request):
        """
        Agrega al request al empleado si el usuario logueado es un empleado.
        """

        if not request.user.is_anonymous() and not request.path.startswith(reverse('admin:index')):
            try:
                request.empleado = request.user.empleado
            except Empleado.DoesNotExist:
                pass
