from django.db import models
from django.utils.translation import ugettext_lazy as _lazy


class Iglesia(models.Model):
    """
    Modelo para guardar la información de las iglesias gestionadas por la aplicación.
    """

    nombre = models.CharField(_lazy('nombre'), max_length=200)
    fecha_registro = models.DateTimeField(_lazy('fecha de registro'), auto_now_add=True)

    class Meta:
        verbose_name = _lazy('iglesia')
        verbose_name_plural = _lazy('iglesias')

    def __str__(self):
        return self.nombre
