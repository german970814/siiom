'''
Created on Apr 1, 2011

@author: Migue
'''

from django.contrib import admin
from grupos.models import Red
from grupos.models import Grupo
from grupos.models import ReunionGAR
from grupos.models import ReunionDiscipulado

class GrupoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']


admin.site.register(Red)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(ReunionGAR)
admin.site.register(ReunionDiscipulado)
