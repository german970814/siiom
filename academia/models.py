from django.db import models


class Modulo(models.Model):
    nombre = models.CharField(max_length=20)
    porcentaje = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre + " - " + str(self.porcentaje)


class Sesion(models.Model):
    nombre = models.CharField(max_length=500)
    modulo = models.ForeignKey(Modulo)

    def __str__(self):
        return self.nombre + " - " + self.modulo.nombre


class Curso(models.Model):
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
        return self.nombre + " - " + self.profesor.nombre


class Matricula(models.Model):
    fechaInicio = models.DateField()
    notaDefinitiva = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    pago = models.PositiveIntegerField(default=0)
    estudiante = models.ForeignKey('miembros.Miembro', unique=True)
    curso = models.ForeignKey(Curso)
    moduloActual = models.ForeignKey(Modulo, null=True, blank=True, related_name='modulo_actual', verbose_name="Modulo")
    sesiones = models.ManyToManyField(Sesion, through='AsistenciaSesiones')
    modulos = models.ManyToManyField(Modulo, through='Reporte', related_name='reporte_modulo')

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

    def __str__(self):
        return self.estudiante.nombre + " - " + self.curso.nombre


class AsistenciaSesiones(models.Model):
    matricula = models.ForeignKey(Matricula)
    sesion = models.ForeignKey(Sesion)
    asistencia = models.BooleanField(default=False)
    tarea = models.BooleanField(default=False)
    fecha = models.DateField()

    def __str__(self):
        return self.matricula.estudiante.nombre

    class Meta:
        get_latest_by = 'fecha'
        unique_together = ('matricula', 'sesion')


class Reporte(models.Model):
    matricula = models.ForeignKey(Matricula)
    modulo = models.ForeignKey(Modulo)
    nota = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return self.matricula.estudiante.nombre

    class Meta:
        ordering = ['id']
        unique_together = ('matricula', 'modulo')
