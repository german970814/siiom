from django.conf.urls import include, patterns, url
from .views import *
from grupos.views import editarHorarioReunionGrupo, reportarReunionGrupo, reportarReunionGrupoAdmin, reportarReunionDiscipulado, registrarPagoGrupo,registrarPagoDiscipulado

urlpatterns = [
    url(r'^$', miembroInicio, name="miembro_inicio"),
    url(r'^agregar_miembro/$', liderAgregarMiembro, name="agregar_miembro"),
    url(r'^listar_miembros/$', liderListarMiembrosGrupo, name="listar_miembros"),  # No se usa actualmente
    url(r'^editar_miembros/$', liderEditarMiembros, name="editar_miembros"),  # No se usa actualmente
    url(r'^editar_miembro/(\d+)/$', editarMiembro, name="editar_miembro"),
    url(r'^transladar_miembros/$', liderTransaldarMiembro, name="transladar_miembros"),  # No se usa actualmente
    # url(r'^editar_perfil/$', liderEditarPerfil, name="editar_perfil"),
    url(r'^perfil/(?P<pk>\d*)$', liderEditarPerfil, name="editar_perfil"),
    url(r'^cambiar_contrasena/$', cambiarContrasena, name="cambiar_contrasena"),
    url(r'^llamadas_pendientes/lider/$', liderLlamadasPendientesVisitantesGrupo, name="llamadas_pendientes_lider"),
    url(r'^llamadas_pendientes/agente/$', llamadasPendientesVisitantes, name="llamadas_pendientes_agente"),  # aqui
    url(r'^registrar_llamada/lider/$', liderLlamarVisitas, name="registrar_llamada_lider"),
    url(r'^registrar_llamada/agente/$', llamarVisitas, name="registrar_llamada_agente"),
    url(r'^promover_visitantes/$', liderPromoverVisitantesGrupo, name="promover_visitantes"),
    url(r'^grupo/(?P<pk>\d*)$', editarHorarioReunionGrupo, name="editar_grupo"),
    url(r'^reportar_reunion_grupo/$', reportarReunionGrupo, name="reportar_reunion_grupo"),
    url(r'^reportar_reunion_grupo_admin/$', reportarReunionGrupoAdmin, name="reportar_reunion_grupo_admin"),
    # url(r'^perfil/(\d+)/$',  perfilMiembro, name="perfil"),
    url(r'^reportar_reunion_discipulado/$', reportarReunionDiscipulado, name="reportar_reunion_discipulado"),
    url(r'^confirmar_ofrenda_gar/(\d+)/$', registrarPagoGrupo, name="confirmar_ofrenda_gar"),
    url(r'^confirmar_ofrenda_discipulado/(\d+)/$', registrarPagoDiscipulado, name="confirmar_ofrenda_discipulado"),
    url(r'^asignar_grupo/(\d+)/$', asignarGrupo, name="asignar_grupo"),
    url(r'^crear_zona/$', crearZona, name="crear_zona"),
    url(r'^editar_zona/(?P<pk>\d+)$', editarZona, name="editar_zona"),
    url(r'^listar_zonas/$', listarZonas, name="listar_zonas"),
    url(r'^barrios/(\d+)/$', barriosDeZona, name="barrios"),
    url(r'^crear_barrio/(\d+)/$', crearBarrio, name="crear_barrio"),
    url(r'^editar_barrio/(?P<id>\d+)/(?P<pk>\d+)$', editarBarrio, name="editar_barrio"),
    url(r'^crear_escalafon/$', crearEscalafon, name="crear_escalafon"),
    url(r'^editar_escalafon/(?P<pk>\d+)$', editarEscalafon, name="editar_escalafon"),
    url(r'^listar_escalafones/$', listarEscalafones, name="listar_escalafones"),
    url(r'^promover_escalafon/$', promoverMiembroEscalafon, name="promover_escalafon"),
    url(r'^agregar_paso/$', agregarPasoMiembro, name="agregar_paso"),
    url(r'^listar_pasos/$', listarPasos, name="listar_pasos"),
    url(r'^editar_paso/(?P<pk>\d+)$', editarPaso, name="editar_paso"),
    url(r'^crear_tipo_miembro/$', crearTipoMiembro, name="crear_tipo_miembro"),
    url(r'^listar_tipo_miembro/$', listarTipoMiembro, name="listar_tipo_miembro"),
    url(r'^editar_tipo_miembro/(?P<pk>\d+)$', editarTipoMiembro, name="editar_tipo_miembro"),
    url(r'^cambiar_tipo_miembro/(\d+)/$', cambiarMiembroDeTipoMiembro, name="cambiar_tipo_miembro"),
    url(r'^detalles_llamada/$', listarDetallesLlamada, name="detalles_llamada"),
    url(r'^agregar_detalle_llamada/$', AgregarDetalleLlamada, name="agregar_detalle_llamada"),
    url(r'^editar_detalle_llamada/(?P<pk>\d+)$', editarDetalleLlamada, name="editar_detalle_llamada"),
    url(r'^graduar_alumno/$', graduarAlumno, name="graduar_alumno"),
    url(r'^asignar_usuario/(\d+)/$', crearUsuarioMimembro, name="asignar_grupo"),
    url(r'^eliminar_cambio_tipo/(\d+)/$', eliminarCambioTipoMiembro, name="eliminar_cambio_tipo"),  # No usada actualmente
    url(r'^cumplimiento_pasos/$', cumplimientoPasos, name="cumplimiento_pasos"),
    url(r'^discipulos/(?P<pk>\d*)$', ver_discipulos, name="ver_discipulos"),
    url(r'^informacion_iglesia/(?P<pk>\d*)$', ver_informacion_miembro, name="ver_informacion"),
]