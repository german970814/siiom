from django.db import models


class MiembroManager(models.Manager):
    """
    Manager para los miembros
    """

    def lideres(self):
        from .models import CambioTipo
        cambios = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='lider').values_list('miembro', flat=True)
        return self.filter(id__in=cambios)

    def visitas(self, *args, **kwargs):
        from .models import CambioTipo, TipoMiembro
        visita = TipoMiembro.objects.filter(nombre__iexact='visita')
        return self.annotate(
            tipos=models.Count('miembro_cambiado')
        ).filter(
            tipos=1, miembro_cambiado__nuevoTipo=visita,
            **kwargs
        )

