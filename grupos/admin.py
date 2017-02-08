'''
Created on Apr 1, 2011

@author: Migue
'''

from django.contrib import admin
from treebeard.admin import TreeAdmin
# from treebeard.forms import movenodeform_factory
from .models import Red
from .models import Grupo
from .models import ReunionGAR
from .models import ReunionDiscipulado
from .models import Predica


class GrupoAdmin(admin.ModelAdmin):
    # form = movenodeform_factory(Grupo)
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
