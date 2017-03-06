from django.conf.urls import url

from . import views, api
from grupos.views import editar_horario_reunion_grupo


urlpatterns = [
    url(r'^$', views.miembro_inicio, name="miembro_inicio"),
    url(r'^perfil/(?P<pk>\d*)$', views.editar_perfil_miembro, name="editar_perfil"),
    url(r'^cambiar_contrasena/$', views.cambiar_contrasena_miembro, name="cambiar_contrasena"),
    url(r'^grupo/(?P<pk>\d*)$', editar_horario_reunion_grupo, name="editar_grupo"),
    url(r'^asignar_grupo/(\d+)/$', views.asignar_grupo, name="asignar_grupo"),
    url(r'^crear_zona/$', views.crear_zona, name="crear_zona"),
    url(r'^editar_zona/(?P<pk>\d+)$', views.editar_zona, name="editar_zona"),
    url(r'^listar_zonas/$', views.listar_zonas, name="listar_zonas"),
    url(r'^barrios/(\d+)/$', views.barrios_zona, name="barrios"),
    url(r'^crear_barrio/(\d+)/$', views.crear_barrio, name="crear_barrio"),
    url(r'^editar_barrio/(?P<id>\d+)/(?P<pk>\d+)$', views.editar_barrio, name="editar_barrio"),
    url(r'^crear_escalafon/$', views.crear_escalafon, name="crear_escalafon"),
    url(r'^editar_escalafon/(?P<pk>\d+)$', views.editar_escalafon, name="editar_escalafon"),
    url(r'^listar_escalafones/$', views.listar_escalafones, name="listar_escalafones"),
    url(r'^promover_escalafon/$', views.promover_miembro_escalafon, name="promover_escalafon"),
    url(r'^agregar_paso/$', views.agregar_paso_miembro, name="agregar_paso"),
    url(r'^listar_pasos/$', views.listar_pasos, name="listar_pasos"),
    url(r'^editar_paso/(?P<pk>\d+)$', views.editar_paso, name="editar_paso"),
    url(r'^crear_tipo_miembro/$', views.crear_tipo_miembro, name="crear_tipo_miembro"),
    url(r'^listar_tipo_miembro/$', views.listar_tipos_miembro, name="listar_tipo_miembro"),
    url(r'^editar_tipo_miembro/(?P<pk>\d+)$', views.editar_tipo_miembro, name="editar_tipo_miembro"),
    url(r'^asignar_usuario/(\d+)/$', views.crear_usuario_miembro, name="asignar_usuario"),
    url(r'^eliminar_cambio_tipo/(\d+)/$', views.eliminar_cambio_tipo_miembro, name="eliminar_cambio_tipo"),
    url(r'^cumplimiento_pasos/$', views.cumplimiento_pasos, name="cumplimiento_pasos"),
    url(r'^discipulos/(?P<pk>\d*)$', views.ver_discipulos, name="ver_discipulos"),
    url(r'^informacion_iglesia/(?P<pk>\d*)$', views.ver_informacion_miembro, name="ver_informacion"),
    url(r'^eliminar_foto_perfil/(?P<pk>\d*)$', views.eliminar_foto_perfil, name="eliminar_foto"),

    url(r'^nuevo/$', views.crear_miembro, name='nuevo'),
    url(r'^redes/(?P<pk>\d+)/lideres/$', views.listar_lideres, name='listar_lideres'),
    url(r'^(?P<pk>\d+)/trasladar/$', views.trasladar, name='trasladar'),

    url(r'^api/desvincular_lider/(?P<pk>\d+)/$', api.desvincular_lider_grupo_api, name='desvincular_grupo_api'),
]
