import logging
from django.core.exceptions import DisallowedHost

logger = logging.getLogger(__name__)


class LogNotAllowedHostHeaderMiddleware(object):
    """
    Middleware que se encarga de loguear en consola los headers del request si este es enviado desde un host no
    permitido.
    """

    def process_request(self, request):
        """
        Loguea en consola los headers del request si el host desde el que se envia el request no se encuentra
        autorizado.
        """

        try:
            request.get_host()
        except DisallowedHost:
            logger.info(request.META)
