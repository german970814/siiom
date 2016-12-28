from django.db import models


class IglesiaMixinQuerySet(models.QuerySet):
    """QuerySet para el modelo abstracto IglesiaMixin."""

    def iglesia(self, iglesia):
        """
        Devuelve un queryset con registros filtrados por la iglesia ingresada.
        """

        return self.filter(iglesia=iglesia)
