from django.db import models
from django.contrib.auth.models import Permission


class MiembroQuerySet(models.QuerySet):
    """
    Queryset personalizado para los miembros.
    """

    # TODO cambiar a lideres cuando se borre el metodo del manager
    def lideres2(self):
        """
        Devuelve un queryset con los lideres de una iglesia. Los lideres son los miembros que tengan permiso de lider.
        """

        permiso = Permission.objects.get(codename='es_lider')
        return self.filter(models.Q(usuario__groups__permissions=permiso) | models.Q(usuario__user_permissions=permiso))

    def red(self, red):
        """
        Devuelve un queryset con los miembros filtrados por la red a la cual pertenece el grupo al que asisten como
        miembros.
        """

        return self.filter(grupo__red=red)


class MiembroManager(models.Manager):
    """
    Manager para los miembros.
    """

    # TODO eliminar este metodo
    def lideres(self):
        from .models import CambioTipo
        cambios = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='lider').values_list('miembro', flat=True)
        return self.filter(id__in=cambios)

    def lideres_disponibles(self):
        """
        Devuelve un queryset con los lideres que no se encuentran liderando grupo.
        """

        disponibles = self.filter(grupo_lidera__isnull=True).lideres2()

        return disponibles

    def lideres_red(self, red):
        """
        Devuelve un queryset con los lideres de la red ingresada.
        """

        return self.filter(models.Q(grupo__red=red) | models.Q(grupo_lidera__red=red)).lideres2()
