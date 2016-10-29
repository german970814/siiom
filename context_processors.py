from django.contrib.sites.models import Site
from miembros.models import Miembro


def site(request):

    site = Site.objects.get_current()
    # miembro = Miembro.objects.get(usuario=request.user)

    data = {
        'sitio': site,
        'dominioIglesia': site.domain,
        'nombreIglesia': site.name,
        # 'id_miembro': miembro.id
    }

    if request.user.is_authenticated():
        try:
            miembro = Miembro.objects.get(usuario=request.user)
            data['id_miembro'] = miembro.id
            data['mi'] = miembro

            draw_mapa = False

            if miembro.grupoLidera() is not None:
                if miembro.grupoLidera().get_position() is None:
                    draw_mapa = True

            data['draw_mapa'] = draw_mapa

        except Miembro.DoesNotExist:
            pass

    return data
