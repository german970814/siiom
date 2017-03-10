'''
Created on Apr 1, 2011

@author: Migue
'''
# Django imports
from django.contrib import admin

# Locale imports
from .models import Red, Grupo, ReunionGAR, ReunionDiscipulado, Predica


class GrupoAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'direccion', 'lideres__nombre', 'lideres__cedula']
    list_display = ('__str__', 'get_estado_display', 'red', )
    list_filter = ('red', 'historiales__estado', )
    list_select_related = ('red', )


class ReunionGARAdmin(admin.ModelAdmin):
    search_fields = ['grupo__nombre']


admin.site.register(Red)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(ReunionGAR, ReunionGARAdmin)
admin.site.register(ReunionDiscipulado)
admin.site.register(Predica)
