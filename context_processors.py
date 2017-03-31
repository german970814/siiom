from contextlib import suppress
from django.contrib.sites.models import Site
from miembros.models import Miembro
from grupos.models import HistorialEstado


def siiom_context_processor(request):
    """
    Procesador de contextos para siiom.
    """

    site = Site.objects.get_current()

    data = {
        'sitio': site,
        'DOMINIO': site.domain,
        'NOMBRE_IGLESIA': site.name,
        'GRUPO_ACTIVO': HistorialEstado.ACTIVO,
        'GRUPO_INACTIVO': HistorialEstado.INACTIVO,
        'GRUPO_SUSPENDIDO': HistorialEstado.SUSPENDIDO
    }

    if hasattr(request, 'user'):
        if request.user.is_authenticated():
            with suppress(Exception):
                miembro = Miembro.objects.get(usuario=request.user)
                draw_mapa = False

                if miembro.grupo_lidera is not None:
                    if miembro.grupo_lidera.get_position() is None:
                        draw_mapa = True

                data['draw_mapa'] = draw_mapa

    return data
