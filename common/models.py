from django.db import models
from django.utils.translation import ugettext_lazy as _lazy

from .managers import IglesiaMixinQuerySet


class IglesiaMixin(models.Model):
    """Modelo abstracto que indica la iglesia a la que pertenece el modelo que la hereda."""

    iglesia = models.ForeignKey('iglesias.Iglesia', verbose_name=_lazy('iglesia'))

    # managers
    objects = IglesiaMixinQuerySet.as_manager()

    class Meta:
        abstract = True
