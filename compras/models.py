from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import RequisicionManager

import re


class Requisicion(models.Model):
    """Modelo que guarda las requisiciones que hechas por los empleados."""

    # opciones
    ALTA = 'A'
    MEDIA = 'M'
    BAJA = 'B'

    OPCIONES_PRIORIDAD = (
        (ALTA, 'ALTA'),
        (MEDIA, 'MEDIA'),
        (BAJA, 'BAJA'),
    )

    PENDIENTE = 'PE'
    PROCESO = 'PR'
    TERMINADA = 'TE'
    ANULADA = 'AN'

    OPCIONES_ESTADO = (
        (PENDIENTE, 'PENDIENTE'),
        (PROCESO, 'PROCESO'),
        (TERMINADA, 'TERMINADA'),
        (ANULADA, 'RECHAZADA'),
    )

    EFECTIVO = 'E'
    CREDITO = 'C'

    OPCIONES_FORMA_PAGO = (
        (EFECTIVO, 'EFECTIVO'),
        (CREDITO, 'CRÉDITO'),
    )

    DATA_SET = {
        'digitada': 'Digitada por Empleado y en Jefe de Departamento',
        'administrativo': 'En Jefe Administrativo',
        'compras': 'En Área de Compras',
        'departamento': 'En Jefe de Departamento',
        'rechaza_administrativo': 'Rechazada por Jefe Administrativo',
        'rechaza_compras': 'Rechazada por Usuario de compras %s',
        'rechaza_departamento': 'Rechazada por Jefe de Departamento',
        'terminada': 'Requisicion en su etapa finalizada'
    }

    fecha_ingreso = models.DateTimeField(verbose_name=_('fecha de ingreso'), auto_now_add=True)
    empleado = models.ForeignKey('organizacional.Empleado', verbose_name=_('empleado'))
    observaciones = models.TextField(verbose_name=_('observaciones'))
    prioridad = models.CharField(max_length=1, verbose_name=_('prioridad'), choices=OPCIONES_PRIORIDAD)
    estado = models.CharField(max_length=2, verbose_name=_('estado'), choices=OPCIONES_ESTADO, default=PENDIENTE)

    fecha_pago = models.DateField(verbose_name=_('fecha de pago'), blank=True, null=True)
    form_pago = models.CharField(
        max_length=1, verbose_name=_('forma de pago'), blank=True, choices=OPCIONES_FORMA_PAGO
    )

    objects = RequisicionManager()

    class Meta:
        verbose_name = _('requisición')
        verbose_name_plural = _('requisiciones')

    def __str__(self):
        return "{0}".format(self.id)

    def __len__(self):
        cls = self.__class__
        rastreo = self.get_rastreo()
        if rastreo == cls.DATA_SET['digitada']:
            return 1
        elif rastreo == cls.DATA_SET['departamento']:
            return 2
        elif rastreo == cls.DATA_SET['compras']:
            return 3
        elif rastreo == cls.DATA_SET['administrativo']:
            return 4
        return 0

    def crear_historial(self, empleado, estado, observacion=''):
        """
        Método para crear el historial de una requisicion y devuelve el objeto de Historial
        sin guardar
        """
        historia = Historial()
        historia.empleado = empleado
        historia.observacion = observacion
        historia.estado = estado
        historia.requisicion = self
        return historia

    def get_rastreo(self):
        """
        Método de rastreo que determina en que lugar se encuentra actualmente una requisición
        (nombre dado por Google)
        """
        if self.estado == self.__class__.TERMINADA:
            return self.__class__.DATA_SET['terminada']
        if self.historial_set.all():
            ultimo = self.historial_set.last()
            if ultimo.estado == Historial.APROBADA:
                if ultimo.empleado.usuario.has_perm('organizacional.es_compras') \
                   and ultimo.empleado.jefe_departamento is True:
                    return self.__class__.DATA_SET['administrativo']
                elif ultimo.empleado.jefe_departamento is True:
                    return self.__class__.DATA_SET['compras']
                elif ultimo.empleado.usuario.has_perm('organizacional.es_compras'):
                    return self.__class__.DATA_SET['administrativo']
            else:
                if ultimo.empleado.jefe_departamento is True \
                   and ultimo.empleado.usuario.has_perm('organizacional.es_compras'):
                    if self.historial_set.count() > 1:
                        return self.__class__.DATA_SET['rechaza_compras'] % ultimo.empleado.__str__()
                    return self.__class__.DATA_SET['rechaza_departamento']
                if ultimo.empleado.jefe_departamento is True:
                    return self.__class__.DATA_SET['rechaza_departamento']
                elif ultimo.empleado.usuario.has_perm('organizacional.es_compras'):
                    return self.__class__.DATA_SET['rechaza_compras'] % ultimo.empleado.__str__()
        return self.__class__.DATA_SET['digitada']

    @property
    def is_anulada(self):
        """
        Retorna Verdadero si la requisicion fue anulada
        """

        if self.estado == self.__class__.ANULADA or \
           any([x for x in self.historial_set.all().distinct() if x.estado == Historial.RECHAZADA]):
            return True
        return False


class DetalleRequisicion(models.Model):
    """Modelo que guarda el detalle de una requisición."""

    EFECTIVO = 'E'
    DEBITO = 'D'
    CREDITO = 'C'

    OPCIONES_FORMA_PAGO = (
        (EFECTIVO, 'EFECTIVO'),
        (DEBITO, 'DÉBITO'),
        (CREDITO, 'CRÉDITO'),
    )

    cantidad = models.PositiveIntegerField(verbose_name=_('cantidad'), blank=True, null=True)
    descripcion = models.TextField(verbose_name=_('descripción'))
    referencia = models.CharField(max_length=50, verbose_name=_('referencia'), blank=True)
    marca = models.CharField(max_length=100, verbose_name=_('marca'), blank=True)
    valor_aprobado = models.PositiveIntegerField(verbose_name=_('valor aprobado'), blank=True, null=True)
    total_aprobado = models.PositiveIntegerField(verbose_name=_('total aprobado'), blank=True, null=True)
    forma_pago = models.CharField(_('forma de pago'), choices=OPCIONES_FORMA_PAGO, max_length=1, blank=True)
    requisicion = models.ForeignKey(Requisicion, verbose_name=_('requisición'))

    class Meta:
        verbose_name = _('detalle de la requisición')
        verbose_name_plural = _('detalles de la requisición')

    def __str__(self):
        return "Requisicion {0} - {1}".format(self.requisicion, self.id)


class Adjunto(models.Model):
    """Modelo que guarda los archivos adjuntos que tienen las requisiciones."""

    def ruta_adjuntos(self, filename):
        match = re.compile(r'[a-zA-ZñNáÁéÉíÍóÓúÚ\s0-9_]')
        data_name = filename.split('.')
        ext = data_name[len(data_name) - 1]
        del data_name[data_name.index(ext)]
        name = ''.join(match.findall(''.join(data_name)))
        filename = name + '.' + ext
        return 'compras/requisicion_{}/{}'.format(self.requisicion.id, filename)

    archivo = models.FileField(verbose_name=_('archivo'), upload_to=ruta_adjuntos)
    requisicion = models.ForeignKey(Requisicion, verbose_name=_('requisición'))

    class Meta:
        verbose_name = _('adjunto')
        verbose_name_plural = _('adjuntos')

    def __str__(self):
        return "{0}".format(self.id)


class Historial(models.Model):
    """"Modelo que guarda la historia de cuando y quien modifica una requisicion."""

    # opciones
    APROBADA = 'A'
    RECHAZADA = 'R'
    OPCIONES_ESTADO = (
        (APROBADA, 'Aprobada'),
        (RECHAZADA, 'Rechazada'),
    )

    requisicion = models.ForeignKey(Requisicion, verbose_name=_('requisición'))
    empleado = models.ForeignKey('organizacional.Empleado', verbose_name=_('empleado'))
    fecha = models.DateTimeField(verbose_name=_('fecha'), auto_now_add=True)
    observacion = models.TextField(verbose_name=_('observación'), blank=True)
    estado = models.CharField(max_length=1, verbose_name=_('estado'), choices=OPCIONES_ESTADO)

    class Meta:
        verbose_name = _('historial')
        verbose_name_plural = _('historial')

    def __str__(self):
        return "Requisicion {0} - {1}".format(self.requisicion, self.id)
