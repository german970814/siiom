from django.core.urlresolvers import reverse
from django.http import Http404


class IglesiaMiddleware(object):
    """
    Middleware que se encarga de agregar al request la iglesia a la cual pertenece el usuario logueado.
    """

    def process_request(self, request):
        """
        Agrega al request la iglesia a la que pertenece el usuario logueado. Si el usuario no pertenece a ninguna
        iglesia se levanta un 404.
        """

        if not request.user.is_anonymous() and not request.path.startswith(reverse('admin:index')):
            if getattr(request, 'miembro', None):
                request.iglesia = request.miembro.iglesia
            elif getattr(request, 'empleado', None):
                request.iglesia = request.empleado.iglesia
            else:
                raise Http404
