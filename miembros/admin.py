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

class miembroAdmin(admin.ModelAdmin):
	list_display = ('id','cedula','nombre','primerApellido','segundoApellido', 'usuario')
	search_fields = ('cedula','nombre','primerApellido','segundoApellido', 'email', 'usuario__username')

class cambioTipoAdmin(admin.ModelAdmin):
	search_fields = ('miembro__nombre',)

admin.site.register(Zona)
admin.site.register(Barrio)
admin.site.register(Pasos)
admin.site.register(TipoMiembro)
admin.site.register(DetalleLlamada)
admin.site.register(Escalafon)
admin.site.register(Miembro,miembroAdmin)
admin.site.register(CambioTipo, cambioTipoAdmin)
admin.site.register(CambioEscalafon)
admin.site.register(CumplimientoPasos)