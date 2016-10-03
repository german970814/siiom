from django.conf.urls import include, patterns, url
from . import views
from .views import *

urlpatterns = [
    url(r'^(\d+)/$', verGrupo, name="grupo"),
    url(r'^listar_redes/$', listarRedes, name="listar_redes"),
    url(r'^crear_red/$', crearRed, name="crear_red"),
    url(r'^editar_red/(?P<pk>\d+)$', editarRed, name="editar_red"),
    url(r'^listar_grupos/(\d+)/$', gruposDeRed, name="listar_grupos"),
    url(r'^crear_grupo/(\d+)/$', crearGrupo, name="crear_grupo"),
    url(r'^editar_grupo/(?P<pk>\d+)$', editarGrupo, name="editar_grupo"),
    url(r'^listar_predicas/$', listarPredicas, name="listar_predicas"),
    url(r'^crear_predica/$', crearPredica, name="crear_predica"),
    url(r'^editar_predica/(?P<pk>\d+)$', editarPredica, name="editar_predica"),
    url(r'^faltante_confirmar_ofrenda/$', faltante_confirmar_ofrenda, name="faltantes_confirmar_ofrenda"),
    url(r'^faltante_confirmar_ofrenda_discipulado/$',
        faltante_confirmar_ofrenda_discipulado, name="faltantes_confirmar_ofrenda_discipulado"),
    url(r'^ver_reportes/$', ver_reportes_grupo, name="reportes_grupo"),
    url(r'^editar_reporte/(?P<pk>\d+)$', editar_runion_grupo, name="editar_reporte"),

    url(r'^redes/(?P<pk>\d+)/nuevo/$', views.CrearGrupoView.as_view(), name='nuevo'),
    url(r'^(?P<pk>\d+)/transladar/$', views.transladar, name='transladar'),
    url(r'^organigrama/$', views.organigrama_grupos, name='organigrama'),
    url(r'^raiz/$', views.grupo_raiz, name='raiz'),
]
