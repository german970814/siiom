from django.conf.urls import url
from django.views.generic import RedirectView

from . import views, api
from grupos.views import (
    editarHorarioReunionGrupo, reportarReunionGrupo, reportarReunionGrupoAdmin, reportarReunionDiscipulado
)

urlpatterns = [
    url(r'^$', views.miembroInicio, name="miembro_inicio"),
    url(r'^editar_miembro/(\d+)/$', views.editarMiembro, name="editar_miembro"),
    url(r'^editar_perfil/$', RedirectView.as_view(url='/miembro/perfil/')),
    url(r'^perfil/(?P<pk>\d*)$', views.liderEditarPerfil, name="editar_perfil"),
    url(r'^cambiar_contrasena/$', views.cambiarContrasena, name="cambiar_contrasena"),
    url(r'^grupo/(?P<pk>\d*)$', editarHorarioReunionGrupo, name="editar_grupo"),
    url(r'^editar_grupo/$', RedirectView.as_view(url="/miembro/grupo/")),
    url(r'^reportar_reunion_grupo/$', reportarReunionGrupo, name="reportar_reunion_grupo"),
    url(r'^reportar_reunion_grupo_admin/$', reportarReunionGrupoAdmin, name="reportar_reunion_grupo_admin"),
    url(r'^reportar_reunion_discipulado/$', reportarReunionDiscipulado, name="reportar_reunion_discipulado"),
    url(r'^asignar_grupo/(\d+)/$', views.asignarGrupo, name="asignar_grupo"),
    url(r'^crear_zona/$', views.crearZona, name="crear_zona"),
    url(r'^editar_zona/(?P<pk>\d+)$', views.editarZona, name="editar_zona"),
    url(r'^listar_zonas/$', views.listarZonas, name="listar_zonas"),
    url(r'^barrios/(\d+)/$', views.barriosDeZona, name="barrios"),
    url(r'^crear_barrio/(\d+)/$', views.crearBarrio, name="crear_barrio"),
    url(r'^editar_barrio/(?P<id>\d+)/(?P<pk>\d+)$', views.editarBarrio, name="editar_barrio"),
    url(r'^crear_escalafon/$', views.crearEscalafon, name="crear_escalafon"),
    url(r'^editar_escalafon/(?P<pk>\d+)$', views.editarEscalafon, name="editar_escalafon"),
    url(r'^listar_escalafones/$', views.listarEscalafones, name="listar_escalafones"),
    url(r'^promover_escalafon/$', views.promoverMiembroEscalafon, name="promover_escalafon"),
    url(r'^agregar_paso/$', views.agregarPasoMiembro, name="agregar_paso"),
    url(r'^listar_pasos/$', views.listarPasos, name="listar_pasos"),
    url(r'^editar_paso/(?P<pk>\d+)$', views.editarPaso, name="editar_paso"),
    url(r'^crear_tipo_miembro/$', views.crearTipoMiembro, name="crear_tipo_miembro"),
    url(r'^listar_tipo_miembro/$', views.listarTipoMiembro, name="listar_tipo_miembro"),
    url(r'^editar_tipo_miembro/(?P<pk>\d+)$', views.editarTipoMiembro, name="editar_tipo_miembro"),
    url(r'^cambiar_tipo_miembro/(\d+)/$', views.cambiarMiembroDeTipoMiembro, name="cambiar_tipo_miembro"),
    url(r'^asignar_usuario/(\d+)/$', views.crearUsuarioMimembro, name="asignar_usuario"),
    url(r'^eliminar_cambio_tipo/(\d+)/$', views.eliminarCambioTipoMiembro, name="eliminar_cambio_tipo"),
    url(r'^cumplimiento_pasos/$', views.cumplimientoPasos, name="cumplimiento_pasos"),
    url(r'^discipulos/(?P<pk>\d*)$', views.ver_discipulos, name="ver_discipulos"),
    url(r'^informacion_iglesia/(?P<pk>\d*)$', views.ver_informacion_miembro, name="ver_informacion"),
    url(r'^eliminar_foto_perfil/(?P<pk>\d*)$', views.eliminar_foto_perfil, name="eliminar_foto"),

    url(r'^nuevo/$', views.crear_miembro, name='nuevo'),
    url(r'^redes/(?P<pk>\d+)/lideres/$', views.listar_lideres, name='listar_lideres'),
    url(r'^(?P<pk>\d+)/trasladar/$', views.trasladar, name='trasladar'),

    url(r'^api/desvincular_lider/(?P<pk>\d+)/$', api.desvincular_lider_grupo_api, name='desvincular_grupo_api'),
]
