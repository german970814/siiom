from django.db import models
import datetime
from .managers import EncuentroManager


class Encuentro(models.Model):
    """
    Modelo para la creacion de encuentros
    """
    ACTIVO = 'A'
    INACTIVO = 'I'
    OPCIONES_ESTADO = (
        (ACTIVO, 'ACTIVO'),
        (INACTIVO, 'INACTIVO'),
    )

    fecha_inicial = models.DateTimeField(verbose_name='Fecha Inicial')
    fecha_final = models.DateField(verbose_name='Fecha Final')
    hotel = models.CharField(max_length=100, verbose_name='Hotel')
    grupos = models.ManyToManyField('grupos.Grupo', verbose_name='Grupos')
    coordinador = models.ForeignKey('miembros.Miembro',
                                    verbose_name='Coordinador', related_name='encuentros_coordinador')
    tesorero = models.ForeignKey('miembros.Miembro', verbose_name='Tesorero', related_name='encuentros_tesorero')
    direccion = models.CharField(max_length=100, verbose_name='Direccion', blank=True)
    observaciones = models.TextField(verbose_name='Observaciones', blank=True)
    dificultades = models.TextField(verbose_name='Dificultades', blank=True)
    estado = models.CharField(max_length=1, choices=OPCIONES_ESTADO, default=ACTIVO, verbose_name='Estado')

    objects = EncuentroManager()

    def __str__(self):
        return '{0} - {1}'.format(self.fecha_inicial, self.fecha_final)

    def save(self, *args, **kwargs):
        self.hotel = self.hotel.upper()
        super(Encuentro, self).save(*args, **kwargs)

    @property
    def en_curso(self):
        if datetime.date.today() >= self.fecha_inicial.date() and datetime.date.today() <= self.fecha_final:
            return True
        return False

    @property
    def acabado(self):
        if datetime.date.today() > self.fecha_final:
            return True
        return False

    @property
    def tiene_asistencia(self):
        if self.encontrista_set.filter(asistio=True):
            return True
        return False


class Encontrista(models.Model):
    """
    Modelo de creacion de encontristas
    """
    MASCULINO = 'M'
    FEMENINO = 'F'
    OPCIONES_GENERO = (
        (MASCULINO, 'MASCULINO'),
        (FEMENINO, 'FEMENINO'),
    )

    primer_nombre = models.CharField(max_length=60, verbose_name='Primer Nombre')
    segundo_nombre = models.CharField(max_length=60, blank=True, verbose_name='Segundo Nombre')
    primer_apellido = models.CharField(max_length=60, verbose_name='Primer Apellido')
    segundo_apellido = models.CharField(max_length=60, blank=True, verbose_name='Segundo Apellido')
    talla = models.CharField(max_length=3, verbose_name='Talla', blank=True)
    genero = models.CharField(max_length=1, choices=OPCIONES_GENERO, verbose_name='Género')
    identificacion = models.IntegerField(verbose_name='Identificación')
    email = models.EmailField(verbose_name='Email')
    grupo = models.ForeignKey('grupos.Grupo', verbose_name='Grupo')
    encuentro = models.ForeignKey(Encuentro, verbose_name='Encuentro')
    asistio = models.BooleanField(default=False, verbose_name='Asistio')

    def __str__(self):
        return '{0} {1} ({3})'.format(self.primer_nombre, self.primer_apellido, self.identificacion)

    def save(self, *args, **kwargs):
        self.primer_nombre = self.primer_nombre.upper()
        self.primer_apellido = self.primer_apellido.upper()
        if self.segundo_nombre:
            self.segundo_nombre = self.segundo_nombre.upper()
        if self.segundo_apellido:
            self.segundo_apellido = self.segundo_apellido.upper()
        super(Encontrista, self).save(*args, **kwargs)
