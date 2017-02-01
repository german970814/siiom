from django.conf.urls import url
from django.views.generic import RedirectView
from . import views
from grupos.views import (
    editarHorarioReunionGrupo, reportarReunionGrupo, reportarReunionGrupoAdmin, reportarReunionDiscipulado
)

urlpatterns = [
    url(r'^$', views.miembroInicio, name="miembro_inicio"),  # revisada
    url(r'^listar_miembros/$', views.liderListarMiembrosGrupo, name="listar_miembros"),  # No se usa actualmente revisada
    url(r'^editar_miembros/$', views.liderEditarMiembros, name="editar_miembros"),  # No se usa actualmente revisada
    url(r'^editar_miembro/(\d+)/$', views.editarMiembro, name="editar_miembro"),  # revisada
    url(r'^editar_perfil/$', RedirectView.as_view(url='/miembro/perfil/')),
    url(r'^perfil/(?P<pk>\d*)$', views.liderEditarPerfil, name="editar_perfil"),  # revisada
    url(r'^cambiar_contrasena/$', views.cambiarContrasena, name="cambiar_contrasena"),  # revisada
    url(r'^llamadas_pendientes/lider/$', views.liderLlamadasPendientesVisitantesGrupo, name="llamadas_pendientes_lider"),  # revisada
    url(r'^llamadas_pendientes/agente/$', views.llamadasPendientesVisitantes, name="llamadas_pendientes_agente"),  # revisada
    url(r'^registrar_llamada/lider/$', views.liderLlamarVisitas, name="registrar_llamada_lider"),  # revisada
    url(r'^registrar_llamada/agente/$', views.llamarVisitas, name="registrar_llamada_agente"),  # revisada
    url(r'^promover_visitantes/$', views.liderPromoverVisitantesGrupo, name="promover_visitantes"),  # revisada
    url(r'^grupo/(?P<pk>\d*)$', editarHorarioReunionGrupo, name="editar_grupo"),  # revisada
    url(r'^editar_grupo/$', RedirectView.as_view(url="/miembro/grupo/")),
    url(r'^reportar_reunion_grupo/$', reportarReunionGrupo, name="reportar_reunion_grupo"),  # revisada
    url(r'^reportar_reunion_grupo_admin/$', reportarReunionGrupoAdmin, name="reportar_reunion_grupo_admin"),  # revisada
    url(r'^reportar_reunion_discipulado/$', reportarReunionDiscipulado, name="reportar_reunion_discipulado"),  # revisada
    url(r'^asignar_grupo/(\d+)/$', views.asignarGrupo, name="asignar_grupo"),  # revisada
    url(r'^crear_zona/$', views.crearZona, name="crear_zona"),  # revisada
    url(r'^editar_zona/(?P<pk>\d+)$', views.editarZona, name="editar_zona"),  # revisada
    url(r'^listar_zonas/$', views.listarZonas, name="listar_zonas"),  # revisada
    url(r'^barrios/(\d+)/$', views.barriosDeZona, name="barrios"),  # revisada
    url(r'^crear_barrio/(\d+)/$', views.crearBarrio, name="crear_barrio"),  # revisada
    url(r'^editar_barrio/(?P<id>\d+)/(?P<pk>\d+)$', views.editarBarrio, name="editar_barrio"),  # revisada
    url(r'^crear_escalafon/$', views.crearEscalafon, name="crear_escalafon"),  # revisada
    url(r'^editar_escalafon/(?P<pk>\d+)$', views.editarEscalafon, name="editar_escalafon"),  # revisada
    url(r'^listar_escalafones/$', views.listarEscalafones, name="listar_escalafones"),  # revisada
    url(r'^promover_escalafon/$', views.promoverMiembroEscalafon, name="promover_escalafon"),  # revisada
    url(r'^agregar_paso/$', views.agregarPasoMiembro, name="agregar_paso"),  # revisada
    url(r'^listar_pasos/$', views.listarPasos, name="listar_pasos"),  # revisada
    url(r'^editar_paso/(?P<pk>\d+)$', views.editarPaso, name="editar_paso"),  # revisada
    url(r'^crear_tipo_miembro/$', views.crearTipoMiembro, name="crear_tipo_miembro"),  # revisada
    url(r'^listar_tipo_miembro/$', views.listarTipoMiembro, name="listar_tipo_miembro"),  # revisada
    url(r'^editar_tipo_miembro/(?P<pk>\d+)$', views.editarTipoMiembro, name="editar_tipo_miembro"),  # revisada
    url(r'^cambiar_tipo_miembro/(\d+)/$', views.cambiarMiembroDeTipoMiembro, name="cambiar_tipo_miembro"),  # revisada
    url(r'^detalles_llamada/$', views.listarDetallesLlamada, name="detalles_llamada"),  # revisada
    url(r'^agregar_detalle_llamada/$', views.AgregarDetalleLlamada, name="agregar_detalle_llamada"),  # revisada
    url(r'^editar_detalle_llamada/(?P<pk>\d+)$', views.editarDetalleLlamada, name="editar_detalle_llamada"),  # revisada
    url(r'^graduar_alumno/$', views.graduarAlumno, name="graduar_alumno"),  # revisada
    url(r'^asignar_usuario/(\d+)/$', views.crearUsuarioMimembro, name="asignar_usuario"),  # revisada
    url(r'^eliminar_cambio_tipo/(\d+)/$', views.eliminarCambioTipoMiembro, name="eliminar_cambio_tipo"),  # No usada revisada
    url(r'^cumplimiento_pasos/$', views.cumplimientoPasos, name="cumplimiento_pasos"),  # revisada
    url(r'^discipulos/(?P<pk>\d*)$', views.ver_discipulos, name="ver_discipulos"),  # revisada
    url(r'^informacion_iglesia/(?P<pk>\d*)$', views.ver_informacion_miembro, name="ver_informacion"),  # revisada
    url(r'^eliminar_foto_perfil/(?P<pk>\d*)$', views.eliminar_foto_perfil, name="eliminar_foto"),  # revisada

    url(r'^nuevo/$', views.crear_miembro, name='nuevo'),
    url(r'^redes/(?P<pk>\d+)/lideres/$', views.listar_lideres, name='listar_lideres'),
    url(r'^(?P<pk>\d+)/trasladar/$', views.trasladar, name='trasladar')
]
