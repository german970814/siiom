from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Departamento(models.Model):
    """Modelo para guardar los departamentos de una iglesia."""

    nombre = models.CharField(_('nombre'), max_length=100)

    class Meta:
        verbose_name = _('departamento')
        verbose_name_plural = _('departamentos')

    def __str__(self):
        return self.nombre.title()


class Area(models.Model):
    """Modelo para guardar las áreas de una iglesia."""

    nombre = models.CharField(_('nombre'), max_length=100)
    departamento = models.ForeignKey(Departamento, verbose_name=_('departamento'), related_name='areas')

    class Meta:
        verbose_name = _('área')
        verbose_name_plural = _('áreas')

    def __str__(self):
        return self.nombre.title()


class Empleado(models.Model):
    """Modelo que guarda las personas que trabajan actualmente para una iglesia."""

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('usuario'))
    areas = models.ManyToManyField(Area, verbose_name=_('áreas'), related_name='empleados')

    class Meta:
        verbose_name = _('empleado')
        verbose_name_plural = _('empleados')

    def __str__(self):
        return self.usuario
