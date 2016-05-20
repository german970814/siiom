from django.contrib import admin
from .models import Modulo
from .models import Sesion
from .models import Curso
from .models import Matricula
from .models import AsistenciaSesiones, Reporte


admin.site.register(Modulo)
admin.site.register(Sesion)
admin.site.register(Curso)
admin.site.register(Matricula)
admin.site.register(AsistenciaSesiones)
admin.site.register(Reporte)
