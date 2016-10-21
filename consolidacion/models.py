from django.db import models
from django.utils.translation import ugettext_lazy as _


class Visita(models.Model):
    """
    Modelo para las visitas que ingresan en el sistema
    """
    primer_nombre = models.CharField(verbose_name=_('primer nombre'), max_length=255)
    segundo_nombre = models.CharField(verbose_name=_('segundo nombre'), max_length=255, blank=True)
    primer_apellido = models.CharField(verbose_name=_('primer apellido'), max_length=255)
    segundo_apellido = models.CharField(verbose_name=_('segundo apellido'), max_length=255, blank=True)
    direccion = models.CharField(verbose_name=_('dirección'), max_length=255, blank=True)
    telefono = models.BigIntegerField(verbose_name=_('teléfono'))
    email = models.EmailField(verbose_name=_('email'), blank=True, unique=True)
    grupo = models.ForeignKey('grupos.Grupo', verbose_name=_('grupo'), blank=True, null=True)
    fecha_ingreso = models.DateField(verbose_name=_('fecha ingreso'), auto_now_add=True)

    def __str__(self):
        return self.primer_nombre.upper() + ' ' + self.primer_apellido.upper()

    def migrar_visita_miembro(self):
        """
        Funcion que migra a la visita a un miembro
        """
        if self.grupo is not None:
            from miembros.models import Miembro
            miembro = Miembro()
            miembro.nombre = self.primer_nombre + ' ' + self.segundo_nombre
            miembro.primerApellido = self.primer_apellido
            miembro.grupo = self.grupo
            miembro.fechaRegistro = self.fecha_ingreso
            miembro.telefono = self.telefono
            if self.segundo_apellido != '':
                miembro.segundoApellido = self.segundo_apellido
            if self.direccion != '':
                miembro.direccion = self.direccion
            if self.email != '':
                miembro.email = self.email
            miembro.save()
            return miembro
        else:
            raise ValueError('No se puede migrar Visita a Miembro si aun no pertenece a grupo')
