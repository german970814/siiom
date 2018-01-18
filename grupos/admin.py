'''
Created on Apr 1, 2011

@author: Migue
'''
# Django imports
from django import forms
from django.contrib import admin
from treebeard.admin import TreeAdmin
from .models import Red, Grupo, ReunionGAR, ReunionDiscipulado, Predica


@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'direccion', 'lideres__nombre', 'lideres__cedula']
    list_display = ('__str__', 'get_estado_display', 'red', )
    list_filter = ('red', 'historiales__estado', )
    list_select_related = ('red', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('lideres', 'historiales')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = Grupo.objects.prefetch_related('historiales', 'lideres').all()
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(ReunionGAR)
class ReunionGARAdmin(admin.ModelAdmin):
    search_fields = ['grupo__nombre']


class GrupoTree(Grupo):
    class Meta:
        proxy = True

@admin.register(GrupoTree)
class GrupoTreeAdmin(TreeAdmin):
    pass


admin.site.register(Red)
admin.site.register(ReunionDiscipulado)
admin.site.register(Predica)
