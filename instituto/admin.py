from django.contrib import admin

from .models import (
    Modulo, Sesion, Curso, Matricula,
    Estudiante, Materia, Salon, Abono
)


admin.site.register(Modulo)
admin.site.register(Sesion)
admin.site.register(Curso)
admin.site.register(Matricula)
admin.site.register(Estudiante)
admin.site.register(Materia)
admin.site.register(Salon)
admin.site.register(Abono)
