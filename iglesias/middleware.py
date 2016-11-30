class IglesiaMiddleware(object):
    """
    Middleware que se encarga de agregar al request la iglesia a la cual pertenece el usuario logueado.
    """

    def process_request(self, request):
        """
        Agrega al request la iglesia a la que pertenece el usuario logueado.
        """

        if hasattr(request, 'miembro'):
            request.iglesia = request.miembro.iglesia
        else:
            request.iglesia = None
