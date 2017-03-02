from django.db import models


class Modulo(models.Model):
    """
    Modelo de creación de modulos en el sistema de la academia.
    """

    nombre = models.CharField(max_length=20)
    porcentaje = models.PositiveIntegerField()

    def __str__(self):
        return '{} - {}'.format(self.nombre.upper(), self.porcentaje)


class Sesion(models.Model):
    """
    Modelo para la creacion de sesiones en la academia, que relacionan con modulo.
    """

    nombre = models.CharField(max_length=500)
    modulo = models.ForeignKey(Modulo)

    def __str__(self):
        return '{} - {}'.format(self.nombre.upper(), self.modulo)


class Curso(models.Model):
    """
    Modelo para guardar los cursos que son dados en la academia.
    """

    opcionesDia = (
        ('0', 'Lunes'),
        ('1', 'Martes'),
        ('2', 'Miercoles'),
        ('3', 'Jueves'),
        ('4', 'Viernes'),
        ('5', 'Sabado'),
        ('6', 'Domingo'),
    )

    opcionesEstado = (
        ('A', 'Abierto'),
        ('C', 'Cerrado'),
    )

    nombre = models.CharField(max_length=20)
    direccion = models.CharField(max_length=50)
    estado = models.CharField(max_length=1, choices=opcionesEstado)
    dia = models.CharField(max_length=1, choices=opcionesDia)
    hora = models.TimeField()
    material = models.TextField(max_length=300)
    profesor = models.ForeignKey('miembros.Miembro')
    red = models.ForeignKey('grupos.Red')
    modulos = models.ManyToManyField(Modulo)

    def __str__(self):
        return '{} - {}'.format(self.nombre.upper(), self.profesor)


class Matricula(models.Model):
    """Modelo para guardar los datos de la matricula de los estudiantes de academia."""

    fechaInicio = models.DateField()
    notaDefinitiva = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    pago = models.PositiveIntegerField(default=0)
    estudiante = models.ForeignKey('miembros.Miembro', unique=True)
    curso = models.ForeignKey(Curso)
    moduloActual = models.ForeignKey(Modulo, null=True, blank=True, related_name='modulo_actual', verbose_name="Modulo")
    sesiones = models.ManyToManyField(Sesion, through='AsistenciaSesiones')
    modulos = models.ManyToManyField(Modulo, through='Reporte', related_name='reporte_modulo')

    def __str__(self):
        return '{} - {}'.format(self.estudiante, self.curso)

    def asistioTodasSesiones(self):
        "Retorna True si un estudiante ha asistido a todas las sesiones del modulo actual en el que esta."

        total = Sesion.objects.filter(modulo=self.moduloActual).count()
        sesiones = self.sesiones.filter(modulo=self.moduloActual).count()
        if total == sesiones:
            return True
        else:
            return False

    def moduloReportado(self):
        "Retorna True si el estudiante ya realizo el examen final del modulo actual."

        try:
            m = self.modulos.get(id=self.moduloActual.id)
            if m:
                return True
            return True
        except:
            return False


class AsistenciaSesiones(models.Model):
    """
    Modelo para guardar la asistencia de los estudiantes matriculados a las sesiones de un modulo.
    """

    matricula = models.ForeignKey(Matricula)
    sesion = models.ForeignKey(Sesion)
    asistencia = models.BooleanField(default=False)
    tarea = models.BooleanField(default=False)
    fecha = models.DateField()

    def __str__(self):
        return self.matricula.estudiante.__str__()

    class Meta:
        get_latest_by = 'fecha'
        unique_together = ('matricula', 'sesion')


class Reporte(models.Model):
    """
    Modelo para guardar las notas de los estudiantes de acuerdo a el modulo.
    """

    matricula = models.ForeignKey(Matricula)
    modulo = models.ForeignKey(Modulo)
    nota = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.matricula.estudiante.__str__()

    class Meta:
        ordering = ['id']
        unique_together = ('matricula', 'modulo')
