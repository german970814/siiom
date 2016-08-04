from django.contrib import admin

from .models import Requisicion, DetalleRequisicion, Adjunto, Historial

admin.site.register(Requisicion)
admin.site.register(DetalleRequisicion)
admin.site.register(Adjunto)
admin.site.register(Historial)
