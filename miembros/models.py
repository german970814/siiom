# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models import Q
from django.core.validators import RegexValidator


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


class Miembro(models.Model):

    def ruta_imagen(self, filename):
        ruta = 'media/profile_pictures/user_%s/%s' % (self.id, filename)
        return ruta

    opcionesGenero = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    opcionesEstado = (
        ('A', 'Activo'),
        ('I', 'Inactivo'),
        ('R', 'Restauración'),
    )

    opcionesEstadoCivil = (
        ('C', 'Casado'),
        ('S', 'Soltero'),
        ('V', 'Viudo'),
        ('D', 'Divorciado'),
    )
    #  autenticacion
    usuario = models.ForeignKey(User, unique=True, null=True, blank=True)
    #  info personal
    nombre = models.CharField(max_length=30)
    primerApellido = models.CharField(max_length=20, verbose_name="primer apellido")
    segundoApellido = models.CharField(max_length=20, verbose_name="segundo apellido", null=True, blank=True)
    genero = models.CharField(max_length=1, choices=opcionesGenero, verbose_name='género')
    telefono = models.CharField(max_length=50, null=True, blank=True, verbose_name='teléfono')
    celular = models.CharField(max_length=50, null=True, blank=True)
    fechaNacimiento = models.DateField(verbose_name="fecha de nacimiento", null=True, blank=True)
    cedula = models.CharField(
        max_length=25,
        unique=True,
        verbose_name='cédula',
        validators=[RegexValidator(r'^[0-9]+$', "Se aceptan solo numeros")]
    )
    direccion = models.CharField(max_length=50, null=True, blank=True, verbose_name='dirección')
    barrio = models.ForeignKey(Barrio, null=True, blank=True)
    email = models.EmailField(unique=True)
    profesion = models.CharField(max_length=20, null=True, blank=True, verbose_name='profesión')
    estadoCivil = models.CharField(
        max_length=1,
        choices=opcionesEstadoCivil,
        null=True, blank=True,
        verbose_name="estado civil"
    )
    conyugue = models.ForeignKey('self', related_name='casado_con', null=True, blank=True, verbose_name='cónyugue')
    foto_perfil = models.ImageField(upload_to=ruta_imagen, null=True, blank=True)
    portada = models.ImageField(upload_to=ruta_imagen, null=True, blank=True)
    #  info iglesia
    convertido = models.BooleanField(default=False)
    estado = models.CharField(max_length=1, choices=opcionesEstado)
    pasos = models.ManyToManyField(Pasos, through='CumplimientoPasos', blank=True)
    escalafon = models.ManyToManyField(Escalafon, through='CambioEscalafon')
    grupo = models.ForeignKey('grupos.Grupo', null=True, blank=True)  # grupo al que pertenece
    #  info GAR
    asignadoGAR = models.BooleanField(default=False, verbose_name="asignado a GAR")
    asisteGAR = models.BooleanField(default=False, verbose_name="asiste a GAR")
    noInteresadoGAR = models.BooleanField(default=False, verbose_name="no interesado en GAR")
    fechaAsignacionGAR = models.DateField(null=True, blank=True, verbose_name='fecha de asignación a GAR')
    #  Llamada Lider
    fechaLlamadaLider = models.DateField(null=True, blank=True, verbose_name='fecha de llamada del líder')
    detalleLlamadaLider = models.ForeignKey(
        DetalleLlamada,
        null=True,
        blank=True,
        related_name='llamada_lider',
        verbose_name='detalle de llamada del líder'
    )
    observacionLlamadaLider = models.TextField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name='observación de llamada del líder'
    )
    #  Primera llamada
    fechaPrimeraLlamada = models.DateField(null=True, blank=True, verbose_name="fecha de primera llamada")
    detallePrimeraLlamada = models.ForeignKey(
        DetalleLlamada,
        null=True,
        blank=True,
        related_name='primera_llamada',
        verbose_name="detalle de primera llamada"
    )
    observacionPrimeraLlamada = models.TextField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name='observación de primera llamada'
    )
    #  Segunda Llamada
    fechaSegundaLlamada = models.DateField(null=True, blank=True, verbose_name="fecha de segunda llamada")
    detalleSegundaLlamada = models.ForeignKey(
        DetalleLlamada,
        null=True,
        blank=True,
        related_name='segunda_llamada',
        verbose_name="detalle de segunda llamada"
    )
    observacionSegundaLlamada = models.TextField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name='observación de segunda llamada'
    )
    fechaRegistro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre + " - " + self.primerApellido + '(' + str(self.cedula) + ')'

    def grupoLidera(self):
        """
        Devuelve el grupo al cual lidera el miembro o su conyugue.
        Si al miembro no se le ha asignado ningun grupo devuelve None.
        """

        from grupos.models import Grupo
        try:
            if self.conyugue:
                return Grupo.objects.get(
                    Q(lider1=self) | Q(lider1=self.conyugue) | Q(lider2=self) | Q(lider2=self.conyugue)
                )
            else:
                return Grupo.objects.get(Q(lider1=self) | Q(lider2=self))
        except:
            return None

    def discipulos(self):
        """Devuelve los discipulos del miembro (queryset) sino tiene, devuelve una lista vacia."""

        lideres = CambioTipo.objects.filter(nuevoTipo__nombre__iexact='lider').values('miembro')
        grupo = self.grupoLidera()
        if grupo:
            return grupo.miembro_set.filter(id__in=lideres)
        else:
            return []

    def pastores(self):
        """Devuelve los indices de los pastores que se encuentran por encima del miembro."""

        grupo_actual = self.grupo
        tipo_pastor = TipoMiembro.objects.get(nombre__iexact='pastor')
        pastores = []

        lideres = Miembro.objects.filter(id__in=self.grupoLidera().listaLideres())
        for lider in lideres:
            tipos = CambioTipo.objects.filter(miembro=lider, nuevoTipo=tipo_pastor)
            if len(tipos) > 0:
                pastores.append(lider.id)

        sw = True

        while sw:

            if grupo_actual is not None:
                lideres = Miembro.objects.filter(id__in=grupo_actual.listaLideres())

                for lider in lideres:
                    tipos = CambioTipo.objects.filter(miembro=lider, nuevoTipo=tipo_pastor)
                    if len(tipos) > 0:
                        pastores.append(lider.id)

                if grupo_actual.lider1.grupo is None:
                    sw = False
                else:
                    grupo_actual = grupo_actual.lider1.grupo
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
