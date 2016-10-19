from django.conf.urls import include, patterns, url
from . import views
from .views import *

urlpatterns = [
    url(r'^listar_redes/$', listarRedes, name="listar_redes"),  # revisada
    url(r'^crear_red/$', crearRed, name="crear_red"),  # revisada
    url(r'^editar_red/(?P<pk>\d+)$', editarRed, name="editar_red"),  # revisada
    url(r'^listar_predicas/$', listarPredicas, name="listar_predicas"),  # revisada
    url(r'^crear_predica/$', crearPredica, name="crear_predica"),  # revisada
    url(r'^editar_predica/(?P<pk>\d+)$', editarPredica, name="editar_predica"),  # revisada
    url(r'^faltante_confirmar_ofrenda_discipulado/$',
        faltante_confirmar_ofrenda_discipulado, name="faltantes_confirmar_ofrenda_discipulado"),
    url(r'^ver_reportes/$', ver_reportes_grupo, name="reportes_grupo"),
    url(r'^editar_reporte/(?P<pk>\d+)$', editar_runion_grupo, name="editar_reporte"),

    url(r'^raiz/$', views.grupo_raiz, name='raiz'),
    url(r'^redes/(?P<pk>\d+)/$', views.listar_grupos, name='listar'),
    url(r'^(?P<pk>\d+)/editar/$', views.editar_grupo, name='editar'),
    url(r'^redes/(?P<pk>\d+)/nuevo/$', views.crear_grupo, name='nuevo'),
    url(r'^organigrama/$', views.organigrama_grupos, name='organigrama'),
    url(r'^(?P<pk>\d+)/transladar/$', views.transladar, name='transladar'),
    url(r'^sin_confirmar_ofrenda_GAR/$', views.sin_confirmar_ofrenda_GAR, name='sin_confirmar_ofrenda_GAR'),
    url(r'^(?P<pk>\d+)/confirmar_ofrenda_GAR/$', views.confirmar_ofrenda_GAR, name='confirmar_ofrenda_GAR')
]
