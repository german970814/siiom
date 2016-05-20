from django.contrib import admin
from .models import Zona
from .models import Barrio
from .models import Pasos
from .models import TipoMiembro
from .models import DetalleLlamada
from .models import Escalafon
from .models import Miembro
from .models import CambioTipo
from .models import CambioEscalafon
from .models import CumplimientoPasos

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