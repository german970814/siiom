from django.conf.urls import url

from . import views, api

urlpatterns = [
    url(r'^listar_predicas/$', views.listar_predicas, name="listar_predicas"),
    url(r'^crear_predica/$', views.crear_predica, name="crear_predica"),
    url(r'^editar_predica/(?P<pk>\d+)/$', views.editar_predica, name="editar_predica"),
    url(r'^ver_reportes/$', views.ver_reportes_grupo, name="reportes_grupo"),
    url(r'^editar_reporte/(?P<pk>\d+)/$', views.editar_runion_grupo, name="editar_reporte"),

    url(r'^raiz/$', views.grupo_raiz, name='raiz'),
    url(r'^redes/$', views.listar_redes, name='redes_listar'),
    url(r'^redes/nueva/$', views.crear_red, name='red_nueva'),
    url(r'^(?P<pk>\d+)/$', views.detalle_grupo, name='detalle'),
    url(r'^(?P<pk>\d+)/editar/$', views.editar_grupo, name='editar'),
    url(r'^redes/(?P<pk>\d+)/$', views.editar_red, name='red_editar'),
    url(r'^redes/(?P<pk>\d+)/nuevo/$', views.crear_grupo, name='nuevo'),
    url(r'^organigrama/$', views.organigrama_grupos, name='organigrama'),
    url(r'^(?P<pk>\d+)/trasladar/$', views.trasladar, name='trasladar'),
    url(r'^archivar/$', views.archivar_grupo, name='archivar'),
    url(r'^redes/(?P<pk>\d+)/grupos/$', views.listar_grupos, name='listar'),
    url(r'^trasladar_lideres/$', views.trasladar_lideres, name='trasladar_lideres'),
    url(r'^sin_confirmar_ofrenda_GAR/$', views.sin_confirmar_ofrenda_GAR, name='sin_confirmar_ofrenda_GAR'),
    url(r'^reportar_reunion_discipulado/$', views.reportar_reunion_discipulado, name="reportar_reunion_discipulado"),
    url(r'^reportar_reunion_grupo_admin/$', views.reportar_reunion_grupo_admin, name="reportar_reunion_grupo_admin"),
    url(r'^reportar_reunion_grupo/$', views.reportar_reunion_grupo, name="reportar_reunion_grupo"),
    url(r'^(?P<pk>\d+)/confirmar_ofrenda_GAR/$', views.confirmar_ofrenda_GAR, name='confirmar_ofrenda_GAR'),
    url(
        r'^sin_confirmar_ofrenda_discipulado/$', views.sin_confirmar_ofrenda_discipulado,
        name='sin_confirmar_ofrenda_discipulado'
    ),
    url(
        r'^(?P<pk>\d+)/confirmar_ofrenda_discipulado/$', views.confirmar_ofrenda_discipulado,
        name='confirmar_ofrenda_discipulado'
    ),
    url(
        r'^reportar_reunion_discipulado_admin/$', views.admin_reportar_reunion_discipulado,
        name='admin_reportar_reunion_discipulado'
    ),

    url(r'^api/set_position_grupo/(?P<id_grupo>\d+)/$', views.set_position_grupo, name="posicion_grupo"),
    url(r'^api/(?P<pk>\d+)/lideres/$', api.lideres_grupo, name='lideres_api'),
    url(r'^api/(?P<pk>\d+)/miembros/$', api.discipulos_miembros_grupo, name='discipulos_miembros_api'),
]
