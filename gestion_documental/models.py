# Django Packages
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Locale Apps
from .managers import SolicitudRegistroManager


class TipoDocumento(models.Model):
    """Modelo para guardar los tipos de documentos que manejan las distintas áreas de una iglesia."""

    nombre = models.CharField(_('nombre'), max_length=100)
    areas = models.ManyToManyField('organizacional.Area', verbose_name=_('áreas'), related_name='tipos_documento')

    class Meta:
        verbose_name = _('tipo de documento')
        verbose_name_plural = _('tipos de documento')

    def __str__(self):
        return self.nombre.capitalize()

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.lower()
        super(TipoDocumento, self).save(*args, **kwargs)


class PalabraClave(models.Model):
    """Modelo que guarda las palabras claves que se usan en los registros."""

    nombre = models.CharField(_('nombre'), max_length=250, unique=True)

    class Meta:
        verbose_name = _('palabra clave')
        verbose_name_plural = _('palabras claves')

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.lower()
        super(PalabraClave, self).save(*args, **kwargs)


class Registro(models.Model):
    """Modelo para guardar los registros de información de una iglesia."""

    area = models.ForeignKey('organizacional.Area', verbose_name=_('área'), related_name='registros')
    descripcion = models.TextField(_('descripción'))
    fecha = models.DateField(_('fecha'))
    palabras_claves = models.ManyToManyField(
        PalabraClave,
        verbose_name=_('palabras claves'),
        related_name='registros',
        blank=True
    )
    estante = models.IntegerField(verbose_name=_('estante'))
    caja = models.IntegerField(verbose_name=_('caja'))

    class Meta:
        verbose_name = _('registro')
        verbose_name_plural = _('registros')

    def __str__(self):
        return "Estante {0} Caja {1}".format(self.estante, self.caja)

    @property
    def solicitado(self):
        """
        Retorna True si el registro esta solicitado
        """
        if self.solicitudregistro_set.exclude(estado=SolicitudRegistro.DEVUELTO_CONSULTA):
            return True
        return False


class Documento(models.Model):
    """Modelo que guarda los archivos relacionados a un registro."""

    def ruta_archivo(self, filename):
        registro = self.registro
        return 'gestion_documental/area_{}/registro_{}/{}'.format(registro.area.id, registro.id, filename)

    registro = models.ForeignKey(Registro, verbose_name=_('registro'), related_name='documentos')
    tipo_documento = models.ForeignKey(TipoDocumento, verbose_name=_('tipo de documento'), related_name='documentos')
    archivo = models.FileField(_('archivo'), upload_to=ruta_archivo)

    class Meta:
        verbose_name = _('documento')
        verbose_name_plural = _('documentos')

    def __str__(self):
        return "{}".format(self.id)

    @property
    def is_image(self):
        if self.get_absolute_url().endswith('.pdf'):
            return False
        return True

    def get_absolute_url(self):
        """
        Devuelve la ruta url de el documento
        """
        return self.archivo.url


class SolicitudRegistro(models.Model):
    """
    Modelo de solicitud de registros
    """
    PENDIENTE = 'PE'
    ENTREGADO_DIGITADOR = 'ED'
    DEVUELTO_CONSULTA = 'DC'

    OPCIONES_ESTADO = (
        (PENDIENTE, 'PENDIENTE'),
        (ENTREGADO_DIGITADOR, 'ENTREGADO POR DIGITADOR'),
        (DEVUELTO_CONSULTA, 'DEVUELTO POR USUARIO DE CONSULTA'),
    )

    registro = models.ForeignKey(Registro, verbose_name=_('Registro'))
    usuario_solicita = models.ForeignKey(
        'organizacional.Empleado', related_name='solicitudes', verbose_name=_('Solicitante')
    )
    estado = models.CharField(max_length=2, verbose_name=_('Estado Solicitud'), choices=OPCIONES_ESTADO)
    fecha_solicitud = models.DateField(auto_now_add=True, verbose_name=_('Fecha Solicitud'))
    fecha_devolucion = models.DateField(blank=True, verbose_name=_('Fecha Devolución'), null=True)
    comentario = models.TextField(verbose_name=_('Comentario'), blank=True)
    usuario_autoriza = models.ForeignKey(
        'organizacional.Empleado', related_name='autorizaciones', verbose_name=_('Autoriza'),
        blank=True, null=True
    )

    objects = SolicitudRegistroManager()

    class Meta:
        verbose_name = _('Solicitud de Registro')
        verbose_name_plural = _('Solicitudes de Registro')

    def __str__(self):
        return "Solicitud No. {}".format(self.id)
