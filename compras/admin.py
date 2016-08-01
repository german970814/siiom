from django.contrib import admin

from .models import Requisicion, DetalleRequisicion, Adjunto

admin.site.register(Requisicion)
admin.site.register(DetalleRequisicion)
admin.site.register(Adjunto)
