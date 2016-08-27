# Django Package
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

# Locale Apps
from .resources import get_festivos
from .managers import CasoManager

# Python Package
import datetime
import calendar


class Caso(models.Model):
    """
    Modelo de casos para Preguntas, Quejas y Reclamos, el cual tendrá la razón de la
    aplicación
    """

    DIAS_PARA_EXPIRAR = 3  # equivale a 72 horas

    LUNES = 0
    MARTES = 1
    MIERCOLES = 2
    JUEVES = 3
    VIERNES = 4
    SABADO = 5
    DOMINGO = 6

    _DIAS_SEMANA = [LUNES, MARTES, MIERCOLES, JUEVES, VIERNES]

    _FINES_SEMANA = [SABADO, DOMINGO]

    fecha_acontecimiento = models.DateField(verbose_name=_('fecha acontecimiento'), blank=True, null=True)
    nombre = models.CharField(verbose_name=_('nombre'), max_length=255)
    identificacion = models.BigIntegerField(verbose_name=_('identificación'))
    direccion = models.CharField(verbose_name=_('dirección'), max_length=255, blank=True)
    telefono = models.BigIntegerField(verbose_name=_('teléfono'), blank=True, null=True)
    email = models.EmailField(verbose_name=_('email'))
    descripcion = models.TextField(verbose_name=_('descripción'))
    asunto = models.CharField(verbose_name=_('asunto'), max_length=255)
    fecha_registro = models.DateTimeField(verbose_name=_('fecha registro'), auto_now_add=True)
    integrantes = models.ManyToManyField(
        'organizacional.Empleado', verbose_name=_('integrantes'), related_name='casos_implicado',
        blank=True, null=True
    )
    empleado_cargo = models.ForeignKey(
        'organizacional.Empleado', verbose_name=_('empleado a cargo'), related_name='casos_cargo',
        blank=True, null=True
    )
    cerrado = models.BooleanField(default=False, verbose_name=_('cerrado'))
    llave = models.SlugField(verbose_name=_('llave'))
    valido = models.BooleanField(default=False, verbose_name=_('valido'))
    fecha_ingreso_habil = models.DateField(verbose_name=_('fecha ingreso hábil'), blank=True, null=True)

    objects = CasoManager()

    class Meta:
        verbose_name = _('Caso PQR')
        verbose_name_plural = _('Casos PQR')

    def __str__(self):
        return 'Caso #{}'.format(self.id)

    def _validacion_expirada(self):
        """
        Retorna verdadero si no se ha validado dentro de 3 dias
        """
        # si no es valido aun
        if not self.valido:
            hoy = timezone.now().date()
            return hoy > self.fecha_registro.date() + datetime.timedelta(days=3)
        # si es valido ya se acabo el tiempo de validacion
        return True

    def _add_days(self, fecha_conteo):
        """
        Funcion que agrega dias a una fecha para saber si esta en fin de semana o en festivo
        """
        dia_ingreso = calendar.weekday(
            fecha_conteo.year, fecha_conteo.month, fecha_conteo.day
        )
        while calendar.weekday(fecha_conteo.year, fecha_conteo.month, fecha_conteo.day) \
                in self.__class__._FINES_SEMANA or \
                fecha_conteo.date() in get_festivos(self.fecha_registro.year):  # or fecha_conteo
            fecha_conteo += datetime.timedelta(days=1)

        return fecha_conteo

    def get_fecha_expiracion(self):
        """
        Devuelve la fecha en que se expira el caso inicialmente para pasar a presidencia
        """
        if not self.cerrado:
            dia_ingreso = calendar.weekday(
                self.fecha_registro.year, self.fecha_registro.month, self.fecha_registro.day
            )
            if dia_ingreso in self.__class__._FINES_SEMANA or \
               self.fecha_registro.date() in get_festivos(self.fecha_registro.year):
                fecha_conteo = self._add_days(self.fecha_registro)
            else:
                fecha_conteo = self.fecha_registro

            fecha_return = fecha_conteo + datetime.timedelta(days=self.DIAS_PARA_EXPIRAR)

            if calendar.weekday(
               fecha_return.year, fecha_return.month, fecha_return.day
               ) in self.__class__._FINES_SEMANA or \
                    fecha_return in get_festivos(fecha_return.year):
                fecha_return = self._add_days(fecha_return)

            return fecha_return

        return None


class Comentario(models.Model):
    """
    Modelo para guardar cada comentario que se le hace a un CASO o PQR, guardando asi
    todos los metadatos relevantes, y respuestas que genere este caso
    """

    mensaje = models.TextField(verbose_name=_('mensaje'))
    fecha = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha'))
    empleado = models.ForeignKey('organizacional.Empleado', verbose_name=_('empleado'))
    caso = models.ForeignKey(Caso, verbose_name=_('caso'))
    importante = models.BooleanField(default=False, verbose_name=_('importante'))

    def __str__(self):
        return 'Comentario Caso # {0}-{1}'.format(self.caso.id, self.id)


class Invitacion(models.Model):
    """
    Modelo para guardar las posibles invitaciones que se le hagan a los empleados de el
    sistema para invitar a colaborar a un caso
    """

    mensaje = models.TextField(verbose_name=_('mensaje'))
    fecha = models.DateTimeField(auto_now_add=True, verbose_name=_('fecha'))
    emisor = models.ForeignKey(
        'organizacional.Empleado', verbose_name=_('emisor'), related_name='invitaciones_realizadas'
    )
    receptor = models.ForeignKey(
        'organizacional.Empleado', verbose_name=_('receptor'), related_name='invitaciones_recibidas'
    )
    caso = models.ForeignKey(Caso, verbose_name=_('caso'))

    class Meta:
        verbose_name = _('Invitación')
        verbose_name_plural = _('Invitaciones')

    def __str__(self):
        return 'Invitación a {0}, caso {1}'.format(self.receptor.__str__(), self.caso.id)
