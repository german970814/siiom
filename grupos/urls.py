from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^listar_predicas/$', views.listarPredicas, name="listar_predicas"),  # revisada
    url(r'^crear_predica/$', views.crearPredica, name="crear_predica"),  # revisada
    url(r'^editar_predica/(?P<pk>\d+)$', views.editarPredica, name="editar_predica"),  # revisada
    url(r'^ver_reportes/$', views.ver_reportes_grupo, name="reportes_grupo"),  # revisada
    url(r'^editar_reporte/(?P<pk>\d+)$', views.editar_runion_grupo, name="editar_reporte"),  # revisada
    url(r'^api/set_position_grupo/(?P<id_grupo>\d+)$', views.set_position_grupo, name="posicion_grupo"),  # revisada

    url(r'^raiz/$', views.grupo_raiz, name='raiz'),
    url(r'^redes/$', views.listar_redes, name='redes_listar'),
    url(r'^redes/nueva/$', views.crear_red, name='red_nueva'),
    url(r'^(?P<pk>\d+)$', views.detalle_grupo, name='detalle'),
    url(r'^(?P<pk>\d+)/editar/$', views.editar_grupo, name='editar'),
    url(r'^redes/(?P<pk>\d+)/$', views.editar_red, name='red_editar'),
    url(r'^redes/(?P<pk>\d+)/nuevo/$', views.crear_grupo, name='nuevo'),
    url(r'^organigrama/$', views.organigrama_grupos, name='organigrama'),
    url(r'^(?P<pk>\d+)/trasladar/$', views.trasladar, name='trasladar'),
    url(r'^redes/(?P<pk>\d+)/grupos/$', views.listar_grupos, name='listar'),
    url(r'^trasladar_lideres/$', views.trasladar_lideres, name='trasladar_lideres'),
    url(r'^sin_confirmar_ofrenda_GAR/$', views.sin_confirmar_ofrenda_GAR, name='sin_confirmar_ofrenda_GAR'),
    url(r'^(?P<pk>\d+)/confirmar_ofrenda_GAR/$', views.confirmar_ofrenda_GAR, name='confirmar_ofrenda_GAR'),
    url(
        r'^sin_confirmar_ofrenda_discipulado/$', views.sin_confirmar_ofrenda_discipulado,
        name='sin_confirmar_ofrenda_discipulado'
    ),
    url(
        r'^(?P<pk>\d+)/confirmar_ofrenda_discipulado/$', views.confirmar_ofrenda_discipulado,
        name='confirmar_ofrenda_discipulado'
    )
]
