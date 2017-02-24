from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _lazy

from .managers import IglesiaMixinQuerySet


class UtilsModelMixin:
    """
    Mixin de utilidades para los modelos.
    """

    def update(**options):
        """
        Actualiza los datos de el modelo.
        """

        with transaction.atomic():
            for key, value in options.items():
                setattr(self, key, value)
            self.save()


# TODO: Al eliminar el mixin de Iglesia, se debe seguir manteniendo el modelo de UtilsModelMixin a todos los modelos
class IglesiaMixin(UtilsModelMixin, models.Model):
    """Modelo abstracto que indica la iglesia a la que pertenece el modelo que la hereda."""

    iglesia = models.ForeignKey('iglesias.Iglesia', verbose_name=_lazy('iglesia'))

    # managers
    objects = IglesiaMixinQuerySet.as_manager()

    class Meta:
        abstract = True
