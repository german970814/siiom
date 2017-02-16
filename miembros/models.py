# -*- coding:utf-8 -*-
import datetime
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _lazy

from common.models import IglesiaMixin
from .managers import MiembroManager


class Zona(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Barrio(models.Model):
    nombre = models.CharField(max_length=50)
    zona = models.ForeignKey(Zona, null=False)

    def __str__(self):
        return self.nombre + " - " + self.zona.nombre


class Pasos(models.Model):
    nombre = models.CharField(max_length=20)
    prioridad = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre


class TipoMiembro(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


class DetalleLlamada(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=200)

    def __str__(self):
        return self.nombre


class Escalafon(models.Model):
    celulas = models.PositiveIntegerField()
    descripcion = models.TextField(max_length=200)
    logro = models.TextField(max_length=200)
    rango = models.CharField(max_length=50)

    def __str__(self):
        return self.rango


class Miembro(IglesiaMixin, models.Model):
    """
    Modelo para guardar los miembros de una iglesia.
    """

    def ruta_imagen(self, filename):
        ruta = 'media/profile_pictures/user_%s/%s' % (self.id, filename)
        return ruta

    # opciones
    FEMENINO = 'F'
    MASCULINO = 'M'
    GENEROS = (
        (FEMENINO, _lazy('Femenino')),
        (MASCULINO, _lazy('Masculino')),
    )

    ACTIVO = 'A'
    INACTIVO = 'I'
    RESTAURACION = 'R'
    ESTADOS = (
        (ACTIVO, _lazy('Activo')),
        (INACTIVO, _lazy('Inactivo')),
        (RESTAURACION, _lazy('Restauración')),
    )

    VIUDO = 'V'
    CASADO = 'C'
    SOLTERO = 'S'
    DIVORCIADO = 'D'
    ESTADOS_CIVILES = (
        (VIUDO, _lazy('Viudo')),
        (CASADO, _lazy('Casado')),
        (SOLTERO, _lazy('Soltero')),
        (DIVORCIADO, _lazy('Divorciado')),
    )
    #  autenticacion
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_lazy('usuario'), unique=True, null=True, blank=True
    )
    #  info personal
    nombre = models.CharField(_lazy('nombre'), max_length=30)
    primerApellido = models.CharField(_lazy('primer apellido'), max_length=20)
    segundoApellido = models.CharField(_lazy('segundo apellido'), max_length=20, null=True, blank=True)
    genero = models.CharField(_lazy('género'), max_length=1, choices=GENEROS)
    telefono = models.CharField(_lazy('teléfono'), max_length=50, null=True, blank=True)
    celular = models.CharField(_lazy('celular'), max_length=50, null=True, blank=True)
    fechaNacimiento = models.DateField(_lazy('fecha de nacimiento'), null=True, blank=True)
    cedula = models.CharField(
        _lazy('cédula'), max_length=25, unique=True, validators=[RegexValidator(r'^[0-9]+$', "Se aceptan solo numeros")]
    )
    direccion = models.CharField(_lazy('dirección'), max_length=50, null=True, blank=True)
    barrio = models.ForeignKey(Barrio, verbose_name=_lazy('barrio'), null=True, blank=True)
    email = models.EmailField(_lazy('email'), unique=True)
    profesion = models.CharField(_lazy('profesion'), max_length=20, null=True, blank=True)
    estadoCivil = models.CharField(
        _lazy('estado civil'), max_length=1, choices=ESTADOS_CIVILES, null=True, blank=True
    )
    conyugue = models.ForeignKey(
        'self', verbose_name=_lazy('cónyugue'), related_name='casado_con', null=True, blank=True
    )
    foto_perfil = models.ImageField(_lazy('foto perfil'), upload_to=ruta_imagen, null=True, blank=True)
    portada = models.ImageField(_lazy('portada'), upload_to=ruta_imagen, null=True, blank=True)
    #  info iglesia
    convertido = models.BooleanField(_lazy('convertido'), default=False)
    estado = models.CharField(_lazy('estado'), max_length=1, choices=ESTADOS)
    pasos = models.ManyToManyField(Pasos, through='CumplimientoPasos', verbose_name=_lazy('pasos'), blank=True)
    escalafon = models.ManyToManyField(Escalafon, through='CambioEscalafon', verbose_name=_lazy('escalafón'))
    grupo = models.ForeignKey(
        'grupos.Grupo', verbose_name=_lazy('grupo'),
        related_name='miembros', null=True, blank=True
    )  # grupo al que pertenece
    grupo_lidera = models.ForeignKey(
        'grupos.Grupo', verbose_name=_lazy('grupo que lidera'),
        related_name='lideres', null=True, blank=True
    )
    #  info GAR
    asignadoGAR = models.BooleanField(_lazy('asignado a GAR'), default=False)
    asisteGAR = models.BooleanField(_lazy('asiste a GAR'), default=False)
    noInteresadoGAR = models.BooleanField(_lazy('no interesado en GAR'), default=False)
    fechaAsignacionGAR = models.DateField(_lazy('fecha de asignación a GAR'), null=True, blank=True)
    #  Llamada Lider
    fechaLlamadaLider = models.DateField(_lazy('fecha de llamada del líder'), null=True, blank=True)
    detalleLlamadaLider = models.ForeignKey(
        DetalleLlamada, verbose_name=_lazy('detalle de llamada del líder'), null=True,
        blank=True, related_name='llamada_lider'
    )
    observacionLlamadaLider = models.TextField(
        _lazy('observación de llamada del líder'), max_length=300, null=True, blank=True
    )
    #  Primera llamada
    fechaPrimeraLlamada = models.DateField(_lazy('fecha de primera llamada'), null=True, blank=True)
    detallePrimeraLlamada = models.ForeignKey(
        DetalleLlamada, verbose_name=_lazy('detalle de primera llamada'), null=True,
        blank=True, related_name='primera_llamada'
    )
    observacionPrimeraLlamada = models.TextField(
        _lazy('observación de primera llamada'), max_length=300, null=True, blank=True
    )
    #  Segunda Llamada
    fechaSegundaLlamada = models.DateField(_lazy('fecha de segunda llamada'), null=True, blank=True)
    detalleSegundaLlamada = models.ForeignKey(
        DetalleLlamada, verbose_name=_lazy('detalle de segunda llamada'), null=True,
        blank=True, related_name='segunda_llamada'
    )
    observacionSegundaLlamada = models.TextField(
        _lazy('observación de segunda llamada'), max_length=300, null=True, blank=True
    )
    fechaRegistro = models.DateField(_lazy('fecha de registro'), auto_now_add=True)

    # managers
    objects = MiembroManager()

    def __str__(self):
        return "{0} {1} ({2})".format(self.nombre.upper(), self.primerApellido.upper(), self.cedula)

    @property
    def es_director_red(self):
        """
        Indica si el miembro es director de red. Un director de red es un miembro que lidere grupo y sea discipulo
        del pastor presidente.
        """

        if self.grupo_lidera:
            if self.grupo_lidera.get_depth() == 2:
                return True

        return False

    @property
    def es_cabeza_red(self):
        """
        Indica si el miembro es cabeza de red. Un cabeza de red es un miembro que lidera grupo y que es discipulo
        de un director de red.
        """

        return self.grupo_lidera and getattr(self.grupo_lidera, 'get_depth', None) == 3

    def trasladar(self, nuevo_grupo):
        """
        Traslada el miembro actual a un nuevo grupo.
        """

        if nuevo_grupo != self.grupo:
            self.grupo = nuevo_grupo
            self.save()

    def discipulos(self):
        """Devuelve los discipulos del miembro (queryset) sino tiene, devuelve una lista vacia."""

        lideres = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='lider').values('miembro')
        grupo = self.grupo_lidera
        if grupo:
            return grupo.miembros.filter(id__in=lideres)
        else:
            return []

    def pastores(self):
        """Devuelve los indices de los pastores que se encuentran por encima del miembro."""

        grupo_actual = self.grupo
        tipo_pastor = TipoMiembro.objects.get(nombre__iexact='pastor')
        pastores = []

        lideres = self.grupo_lidera.lideres.all()
        for lider in lideres:
            tipos = CambioTipo.objects.filter(miembro=lider, nuevoTipo=tipo_pastor)
            if len(tipos) > 0:
                pastores.append(lider.id)

        sw = True

        while sw:

            if grupo_actual is not None:
                lideres = grupo_actual.lideres.all()

                for lider in lideres:
                    tipos = CambioTipo.objects.filter(miembro=lider, nuevoTipo=tipo_pastor)
                    if len(tipos) > 0:
                        pastores.append(lider.id)

                if grupo_actual.parent is None:
                    sw = False
                else:
                    grupo_actual = grupo_actual.parent
            else:
                sw = False

        return pastores

    class Meta:
        permissions = (
            ("es_agente", "define si un miembro es agente"),
            ("es_lider", "indica si el usuario es lider de un GAR"),
            ("es_maestro", "indica si un usuario es maestro de un curso"),
            ("es_administrador", "es adminisitrador"),
            ("buscar_todos", "indica si un usuario puede buscar miembros"),
            ("puede_editar_miembro", "indica si un usuario puede editar miembros"),
            ("puede_agregar_visitante", "puede agregar miembros visitantes"),
            ("llamada_lider", "puede modificar llamada lider"),
            ("llamada_agente", "puede modificar llamada agente"),
            ("cumplimiento_pasos", "puede registrar el cumplimiento de pasos"),
            ("es_pastor", "indica si un miembro es pastor"),
            ("es_tesorero", "indica si un miembro es tesorero"),
            ("es_coordinador", "indica si un miembro es coordinador"),
        )


class CumplimientoPasos(models.Model):
    miembro = models.ForeignKey(Miembro)
    paso = models.ForeignKey(Pasos)
    fecha = models.DateField()

    def __str__(self):
        return self.miembro.nombre + " - " + self.paso.nombre


class CambioEscalafon(models.Model):
    miembro = models.ForeignKey(Miembro)
    escalafon = models.ForeignKey(Escalafon)
    fecha = models.DateField(default=datetime.datetime.now)

    def __str__(self):
        return self.miembro.nombre + " - " + self.escalafon.rango


class CambioTipo(models.Model):
    miembro = models.ForeignKey(Miembro, related_name='miembro_cambiado')
    autorizacion = models.ForeignKey(Miembro, related_name='miembro_autoriza')
    nuevoTipo = models.ForeignKey(TipoMiembro, related_name='tipo_nuevo', verbose_name="tipo nuevo")
    anteriorTipo = models.ForeignKey(TipoMiembro, related_name='tipo_anterior', null=True, verbose_name="tipo anterior")
    fecha = models.DateField()

    def __str__(self):
        return self.miembro.nombre + " - " + self.nuevoTipo.nombre
