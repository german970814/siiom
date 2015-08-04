'''
Created on Apr 1, 2011

@author: Migue
'''

from django.contrib import admin
from grupos.models import Red
from grupos.models import Grupo
from grupos.models import ReunionGAR
from grupos.models import ReunionDiscipulado
from grupos.models import Predica

class GrupoAdmin(admin.ModelAdmin):
    search_fields = ['nombre']

class ReunionGARAdmin(admin.ModelAdmin):
    search_fields = ['grupo__nombre']

admin.site.register(Red)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(ReunionGAR, ReunionGARAdmin)
admin.site.register(ReunionDiscipulado)
admin.site.register(Predica)

