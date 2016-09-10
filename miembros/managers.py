from django.db import models
from django.contrib.auth.models import Permission


class MiembroManager(models.Manager):
    """
    Manager para los miembros.
    """

    def lideres(self):
        from .models import CambioTipo
        cambios = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='lider').values_list('miembro', flat=True)
        return self.filter(id__in=cambios)

    def lideres_disponibles(self):
        """
        Devuelve un queryset con los lideres que no se encuentran liderando grupo.
        """

        from grupos.models import Grupo

        grupos = Grupo.objects.select_related('lider1', 'lider2').all()
        lideres_grupos = []
        for grupo in grupos:
            lideres_grupos.extend(grupo.listaLideres())

        permiso = Permission.objects.get(codename='es_lider')
        lideres = self.filter(
            models.Q(usuario__groups__permissions=permiso) | models.Q(usuario__user_permissions=permiso)
        )

        return lideres.exclude(id__in=lideres_grupos)
