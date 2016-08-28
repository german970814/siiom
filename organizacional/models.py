from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .managers import AreaManager


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

    objects = AreaManager()

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
    cedula = models.BigIntegerField(verbose_name=_('cédula'), unique=True)
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
            ('es_compras', 'Es usuario de compras'),
            ('es_presidente', 'Es presidente'),
        )

    def __str__(self):
        return '{0} {1}'.format(self.primer_nombre.upper(), self.primer_apellido.upper())

    def get_solicitudes(self):
        """
        Retorna las solicitudes actuales
        """
        from gestion_documental.models import SolicitudRegistro as Solicitud
        return self.solicitudes.filter(estado__in=[Solicitud.PENDIENTE, Solicitud.ENTREGADO_DIGITADOR])

    @property
    def is_jefe_comercial(self):
        """
        Retorna Verdadero si el empleado es jefe de el departamento comercial
        """
        if self.jefe_departamento:
            if any(self.areas.filter(departamento__nombre__icontains='comerci')):
                return True
        return False

    @property
    def is_jefe_administrativo(self):
        """
        Retorna verdadero si es jefe administrativo
        """
        if self.jefe_departamento:
            if any(self.areas.filter(departamento__nombre__icontains='administra')):
                return True
        return False

    @property
    def is_jefe_financiero(self):
        """
        Retorna verdadero si el jefe es del departamento financiero
        """
        if self.jefe_departamento:
            if any(self.areas.filter(departamento__nombre__icontains='financi')):
                return True
        return False

    @property
    def is_compras(self):
        """
        Retorna verdadero si el empleado es de el area de compras
        """
        if any(self.areas.filter(nombre__icontains='compra')):
            return True
        return False

    @property
    def is_usuario_pago(self):
        """
        Retorna verdadero si el usuario es encargado de pagos
        """
        if any(
            self.areas.filter(nombre__icontains='contab') | self.areas.filter(nombre__icontains='tesore')
        ):
            return True
        return False

    @property
    def is_servicio_cliente(self):
        """
        Retorna True si el empleado es de el area de servicio al cliente
        """
        return self.areas.filter(nombre__icontains='servicio').exists()
