from django.contrib import admin

from .models import Modulo, Sesion, Curso, Matricula, AsistenciaSesiones, Reporte


admin.site.register(Modulo)
admin.site.register(Sesion)
admin.site.register(Curso)
admin.site.register(Matricula)
admin.site.register(AsistenciaSesiones)
admin.site.register(Reporte)
