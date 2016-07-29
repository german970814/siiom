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

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.lower()
        super(Departamento, self).save(*args, **kwargs)


class Area(models.Model):
    """Modelo para guardar las áreas de una iglesia."""

    nombre = models.CharField(_('nombre'), max_length=100)
    departamento = models.ForeignKey(Departamento, verbose_name=_('departamento'), related_name='areas')

    class Meta:
        verbose_name = _('área')
        verbose_name_plural = _('áreas')

    def __str__(self):
        return self.nombre.title()

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.lower()
        super(Area, self).save(*args, **kwargs)


class Empleado(models.Model):
    """Modelo que guarda las personas que trabajan actualmente para una iglesia."""

    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name=_('usuario'))
    areas = models.ManyToManyField(Area, verbose_name=_('áreas'), related_name='empleados')
    cedula = models.BigIntegerField(verbose_name=_('cédula'))
    primer_nombre = models.CharField(max_length=100, verbose_name=_('primer nombre'))
    segundo_nombre = models.CharField(max_length=100, blank=True, verbose_name=_('segundo nombre'))
    primer_apellido = models.CharField(max_length=100, verbose_name=_('primer apellido'))
    segundo_apellido = models.CharField(max_length=100, blank=True, verbose_name=_('segundo apellido'))
    jefe_departamento = models.BooleanField(verbose_name=_('jefe de departamento'), default=False)

    class Meta:
        verbose_name = _('empleado')
        verbose_name_plural = _('empleados')
        permissions = (
            ('es_administrador_sgd', 'Es Administrador de Sistema Gestion Documental'),
            ('buscar_registros', 'Puede Buscar Registros'),
        )

    def __str__(self):
        return '{0} {1}'.format(self.primer_nombre.upper(), self.primer_apellido.upper())

    def get_solicitudes(self):
        """
        Retorna las solicitudes actuales
        """
        from gestion_documental.models import SolicitudRegistro as Solicitud
        return self.solicitudes.filter(estado__in=[Solicitud.PENDIENTE, Solicitud.ENTREGADO_DIGITADOR])
