from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import RequisicionManager, ParametrosManager

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

    PAGO_PROVEEDOR = 'PP'
    ANTICIPO_PROVEEDOR = 'AP'
    EFECTIVO_PROVEEDOR = 'EP'

    OPCIONES_ESTADO_PAGO = (
        (PAGO_PROVEEDOR, 'PAGO AL PROVEEDOR'),
        (ANTICIPO_PROVEEDOR, 'ANTICIPO AL PROVEEDOR'),
        (EFECTIVO_PROVEEDOR, 'EFECTIVO AL PROVEEDOR'),
    )

    SI = 'SI'
    ESPERA = 'ES'

    OPCIONES_PRESUPUESTO = (
        (SI, 'SI'),
        (ESPERA, 'EN ESPERA'),
    )

    DATA_SET = {
        'digitada': 'Digitada por Empleado y en Jefe de Departamento',
        'administrativo': 'En Jefe Administrativo',
        'compras': 'En Área de Compras',
        'departamento': 'En Jefe de Departamento',
        'financiero': 'En Director Financiero',
        'rechaza_administrativo': 'Rechazada por Jefe Administrativo',
        'rechaza_compras': 'Rechazada por Usuario de compras %s',
        'rechaza_departamento': 'Rechazada por Jefe de Departamento',
        'rechaza_administrativo': 'Rechazada por Jefe Administrativo',
        'terminada': 'Requisicion en su etapa finalizada',
        'pago': 'Esperando usuario encargado de pago',
        'espera_presupuesto': 'A la espera de presupuesto disponible',
        'presidencia': 'En Presidencia',
        'rechaza_presidencia': 'Rechazada por presidencia'
    }

    fecha_ingreso = models.DateTimeField(verbose_name=_('fecha de ingreso'), auto_now_add=True)
    empleado = models.ForeignKey('organizacional.Empleado', verbose_name=_('empleado'))
    observaciones = models.TextField(verbose_name=_('observaciones'))
    asunto = models.CharField(verbose_name=_('asunto'), max_length=255)
    prioridad = models.CharField(max_length=1, verbose_name=_('prioridad'), choices=OPCIONES_PRIORIDAD)
    estado = models.CharField(max_length=2, verbose_name=_('estado'), choices=OPCIONES_ESTADO, default=PENDIENTE)

    fecha_pago = models.DateField(verbose_name=_('fecha de pago'), blank=True, null=True)
    form_pago = models.CharField(
        max_length=1, verbose_name=_('forma de pago'), blank=True, choices=OPCIONES_FORMA_PAGO
    )
    estado_pago = models.CharField(
        max_length=2, verbose_name=_('estado de pago'), blank=True, choices=OPCIONES_ESTADO_PAGO
    )

    presupuesto_aprobado = models.CharField(
        max_length=2, verbose_name=_('presupuesto aprobado'), blank=True, choices=OPCIONES_PRESUPUESTO
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
        elif rastreo == cls.DATA_SET['financiero'] or rastreo == cls.DATA_SET['espera_presupuesto']:
            return 5
        elif rastreo == cls.DATA_SET['pago']:
            return 6
        elif rastreo == cls.DATA_SET['presidencia']:
            return 7
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
            # si está terminada se sale enseguida
            return self.__class__.DATA_SET['terminada']
        if self.historial_set.all():
            # si tiene historial se saca el ultimo
            ultimo = self.historial_set.last()
            # si ya tiene fecha de pago, quiere decir que su proceso está por terminar
            if self.fecha_pago:
                return self.__class__.DATA_SET['pago']
            # siempre y cuando esté aprobada por la ultima persona
            if ultimo.estado == Historial.APROBADA:
                # si la ultima persona en modificar es de compras y ademas es jefe de departamento
                if ultimo.empleado.is_compras and ultimo.empleado.jefe_departamento is True:
                    # si tiene mas de dos historiales ya se encuentra en financiero
                    if self.historial_set.count() >= 3:
                        # si alcanza el tope intercepta presidencia
                        if self.get_total() > Parametros.objects.tope():
                            return self.__class__.DATA_SET['presidencia']
                        return self.__class__.DATA_SET['financiero']
                    # si tiene mas dos historiales está en administrativo
                    if self.historial_set.count() == 2:
                        return self.__class__.DATA_SET['administrativo']
                    # de lo contrario está en compras
                    else:
                        return self.__class__.DATA_SET['compras']
                # si el ultimo empleado fue el presidente
                elif ultimo.empleado.usuario.has_perm('organizacional.es_presidente'):
                    return self.__class__.DATA_SET['financiero']
                # si el ultimo es jefe financiero
                elif ultimo.empleado.is_jefe_financiero:
                    # si tiene una observacion se pone en espera
                    if ultimo.observacion != '' and self.presupuesto_aprobado == self.__class__.ESPERA:
                        return self.__class__.DATA_SET['espera_presupuesto']
                    # de lo contrario pasa a pago
                    return self.__class__.DATA_SET['pago']
                # si el ultimo empleado es jefe administrativo
                # no se tiene en cuenta cuando es == 2 porque solo se da en condicional de arriba
                elif ultimo.empleado.is_jefe_administrativo is True:
                    # si supera el monto establecido pasa a presidencia
                    if self.get_total() > Parametros.objects.tope():
                        return self.__class__.DATA_SET['presidencia']
                    # si tiene mas de dos historiales está en financiero
                    elif self.historial_set.count() > 2:
                        return self.__class__.DATA_SET['financiero']
                    # de lo contrario, está en compras
                    else:
                        return self.__class__.DATA_SET['compras']
                # si es jefe de departamento
                elif ultimo.empleado.jefe_departamento is True:
                    return self.__class__.DATA_SET['compras']
                # si es de compras
                elif ultimo.empleado.is_compras:
                    return self.__class__.DATA_SET['administrativo']
            # si no fue aprobada por la ultima persona
            else:
                # si rechaza la presidencia
                if ultimo.empleado.usuario.has_perm('organizacional:es_presidente'):
                    return self.__class__.DATA_SET['rechaza_presidencia']
                # si rechazo jefe administrativo
                elif ultimo.empleado.is_jefe_administrativo:
                    return self.__class__.DATA_SET['rechaza_administrativo']
                # si rechazo jefe de departamento y es de compras
                elif ultimo.empleado.jefe_departamento is True \
                        and ultimo.empleado.is_compras:
                    return self.__class__.DATA_SET['rechaza_departamento']
                # si rechaza un jefe de departamento
                elif ultimo.empleado.jefe_departamento is True:
                    return self.__class__.DATA_SET['rechaza_departamento']
        # de cualquier otro modo, la requisicion aun no ha sido revisada
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

    def get_total(self):
        """
        Retorna el valor total de la requisicion, con la suma de los totales de todos los detalles
        de la requisicion
        """

        total = 0
        for detalle in self.detallerequisicion_set.all():
            total += detalle.get_valor_total()
        return total


class DetalleRequisicion(models.Model):
    """Modelo que guarda el detalle de una requisición."""

    EFECTIVO = 'E'
    DEBITO = 'D'
    CREDITO = 'C'

    OPCIONES_FORMA_PAGO = (
        (EFECTIVO, 'EFECTIVO'),
        (DEBITO, 'CHEQUE'),
        (CREDITO, 'CRÉDITO'),
    )

    cantidad = models.PositiveIntegerField(verbose_name=_('cantidad'), blank=True, null=True)
    descripcion = models.TextField(verbose_name=_('descripción'))
    referencia = models.CharField(max_length=50, verbose_name=_('referencia'), blank=True)
    marca = models.CharField(max_length=100, verbose_name=_('marca'), blank=True)
    valor_aprobado = models.PositiveIntegerField(verbose_name=_('valor unitario'), blank=True, null=True)
    total_aprobado = models.PositiveIntegerField(verbose_name=_('valor total'), blank=True, null=True)
    forma_pago = models.CharField(_('forma de pago'), choices=OPCIONES_FORMA_PAGO, max_length=1, blank=True)
    requisicion = models.ForeignKey(Requisicion, verbose_name=_('requisición'))

    class Meta:
        verbose_name = _('detalle de la requisición')
        verbose_name_plural = _('detalles de la requisición')

    def __str__(self):
        return "Requisicion {0} - {1}".format(self.requisicion, self.id)

    def save(self, *args, **kwargs):
        if not self.cantidad:
            self.cantidad = 1
        if not self.valor_aprobado:
            self.valor_aprobado = 0
        self.total_aprobado = self.get_valor_total()
        super(DetalleRequisicion, self).save(*args, **kwargs)

    def get_valor_total(self):
        """
        Retorna el valor total de acuerdo a la cantidad y al valor unitario
        """
        if not self.cantidad:
            self.cantidad = 1
        total = self.cantidad * self.valor_aprobado
        return total


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

    def get_name(self):
        """
        Retorna el nombre del archivo
        """
        path = self.archivo._get_path().split('/')
        return path[len(path) - 1]


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


class Parametros(models.Model):
    """
    Modelo para parametrizar ciertos valores de los que dependen los procesos de
    trazabilidad de la aplicacion
    """
    dias_habiles = models.PositiveSmallIntegerField(verbose_name=_('dias hábiles'))
    tope_monto = models.PositiveIntegerField(verbose_name=_('monto tope para presidencia'))

    objects = ParametrosManager()

    class Meta:
        verbose_name = _('parametro')
        verbose_name_plural = _('parametros')

    def __str__(self):
        return '({0})-({1})'.format(self.dias_habiles, self.tope_monto)
