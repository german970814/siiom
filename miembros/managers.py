from django.db import models
from django.contrib.auth.models import Permission


class MiembroQuerySet(models.QuerySet):
    """
    Queryset personalizado para los miembros.
    """

    def red(self, red):
        """
        Devuelve un queryset con los miembros filtrados por la red ingresada. Los miembros se filtran por el grupo al
        que pertencen.
        """

        return self.filter(grupo__red=red)


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

        permiso = Permission.objects.get(codename='es_lider')
        disponibles = self.filter(
            models.Q(usuario__groups__permissions=permiso) | models.Q(usuario__user_permissions=permiso),
            grupo_lidera__isnull=True
        )

        return disponibles
