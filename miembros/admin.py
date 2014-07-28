from django.contrib import admin
from miembros.models import Zona
from miembros.models import Barrio
from miembros.models import Pasos
from miembros.models import TipoMiembro
from miembros.models import DetalleLlamada
from miembros.models import Escalafon
from miembros.models import Miembro
from miembros.models import CambioTipo
from miembros.models import CambioEscalafon
from miembros.models import CumplimientoPasos


admin.site.register(Zona)
admin.site.register(Barrio)
admin.site.register(Pasos)
admin.site.register(TipoMiembro)
admin.site.register(DetalleLlamada)
admin.site.register(Escalafon)
admin.site.register(Miembro)
admin.site.register(CambioTipo)
admin.site.register(CambioEscalafon)
admin.site.register(CumplimientoPasos)