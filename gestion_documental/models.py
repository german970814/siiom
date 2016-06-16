from django.db import models
from django.utils.translation import ugettext_lazy as _


class TipoDocumento(models.Model):
    """Modelo para guardar los tipos de documentos que manejan las distintas áreas de una iglesia."""

    nombre = models.CharField(_('nombre'), max_length=100)
    areas = models.ManyToManyField('organizacional.Area', verbose_name=_('áreas'), related_name='tipos_documento')

    class Meta:
        verbose_name = _('tipo de documento')
        verbose_name_plural = _('tipos de documento')

    def __str__(self):
        return self.nombre.capitalize()


class PalabraClave(models.Model):
    """Modelo que guarda las palabras claves que se usan en los registros."""

    nombre = models.CharField(_('nombre'), max_length=250)

    class Meta:
        verbose_name = _('palabra clave')
        verbose_name_plural = _('palabras claves')

    def __str__(self):
        return self.nombre


class Registro(models.Model):
    """Modelo para guardar los registros de información de una iglesia."""

    area = models.ForeignKey('organizacional.Area', verbose_name=_('área'), related_name='registros')
    descripcion = models.TextField(_('descripción'))
    palabras_claves = models.ManyToManyField(
        PalabraClave,
        verbose_name=_('palabras claves'),
        related_name='registros',
        blank=True
    )

    class Meta:
        verbose_name = _('registro')
        verbose_name_plural = _('registros')


class Documento(models.Model):
    """Modelo que guarda los archivos relacionados a un registro."""

    def ruta_archivo(self, filename):
        registro = self.registro
        return 'gestion_documental/area_{}/registro_{}/{}'.format(registro.area.id, registro.id, self.filename)

    registro = models.ForeignKey(Registro, verbose_name=_('registro'), related_name='documentos')
    tipo_documento = models.ForeignKey(TipoDocumento, verbose_name=_('tipo de documento'), related_name='documentos')
    archivo = models.FileField(_('archivo'), upload_to=ruta_archivo)

    class Meta:
        verbose_name = _('documento')
        verbose_name_plural = _('documentos')
