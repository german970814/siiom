from django.core.urlresolvers import reverse
from .models import Miembro


class MiembroMiddleWare(object):
    """
    Middleware que se encarga de agregar el miembro al request.
    """

    def process_request(self, request):
        """
        Agrega al request el miembro si el usuario logueado es un miembro.
        """

        if not request.user.is_anonymous() and not request.path.startswith(reverse('admin:index')):
            try:
                request.miembro = Miembro.objects.get(usuario=request.user)
            except Miembro.DoesNotExist:
                pass
