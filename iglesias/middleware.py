from django.core.urlresolvers import reverse


class IglesiaMiddleware(object):
    """
    Middleware que se encarga de agregar al request la iglesia a la cual pertenece el usuario logueado.
    """

    def process_request(self, request):
        """
        Agrega al request la iglesia a la que pertenece el usuario logueado.
        """

        if not request.user.is_anonymous() and not request.path.startswith(reverse('admin:index')):
            if hasattr(request, 'miembro'):
                request.iglesia = request.miembro.iglesia
            else:
                request.iglesia = None
