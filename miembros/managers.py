from django.db import models


class MiembroManager(models.Manager):
    """
    Manager para los miembros
    """

    def lideres(self):
        from .models import CambioTipo
        cambios = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='lider').values_list('miembro', flat=True)
        return self.filter(id__in=cambios)
