from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^listar_redes/$', views.listarRedes, name="listar_redes"),  # revisada
    url(r'^crear_red/$', views.crearRed, name="crear_red"),  # revisada
    url(r'^editar_red/(?P<pk>\d+)$', views.editarRed, name="editar_red"),  # revisada
    url(r'^listar_predicas/$', views.listarPredicas, name="listar_predicas"),  # revisada
    url(r'^crear_predica/$', views.crearPredica, name="crear_predica"),  # revisada
    url(r'^editar_predica/(?P<pk>\d+)$', views.editarPredica, name="editar_predica"),  # revisada
    url(r'^ver_reportes/$', views.ver_reportes_grupo, name="reportes_grupo"),  # revisada
    url(r'^editar_reporte/(?P<pk>\d+)$', views.editar_runion_grupo, name="editar_reporte"),  # revisada
    url(r'^api/set_position_grupo/(?P<id_grupo>\d+)$', views.set_position_grupo, name="posicion_grupo"),

    url(r'^raiz/$', views.grupo_raiz, name='raiz'),
    url(r'^redes/(?P<pk>\d+)/$', views.listar_grupos, name='listar'),
    url(r'^(?P<pk>\d+)/editar/$', views.editar_grupo, name='editar'),
    url(r'^redes/(?P<pk>\d+)/nuevo/$', views.crear_grupo, name='nuevo'),
    url(r'^organigrama/$', views.organigrama_grupos, name='organigrama'),
    url(r'^(?P<pk>\d+)/transladar/$', views.transladar, name='transladar'),
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
