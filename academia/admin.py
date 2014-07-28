from django.contrib import admin
from Iglesia.academia.models import Modulo
from Iglesia.academia.models import Sesion
from Iglesia.academia.models import Curso
from Iglesia.academia.models import Matricula
from Iglesia.academia.models import AsistenciaSesiones, Reporte


admin.site.register(Modulo)
admin.site.register(Sesion)
admin.site.register(Curso)
admin.site.register(Matricula)
admin.site.register(AsistenciaSesiones)
admin.site.register(Reporte)
