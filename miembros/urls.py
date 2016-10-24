from django.conf.urls import include, patterns, url
from django.views.generic import RedirectView
from .views import *
from . import views
from grupos.views import editarHorarioReunionGrupo, reportarReunionGrupo, \
    reportarReunionGrupoAdmin, reportarReunionDiscipulado

urlpatterns = [
    url(r'^$', miembroInicio, name="miembro_inicio"),
    url(r'^agregar_miembro/$', liderAgregarMiembro, name="agregar_miembro"),
    url(r'^listar_miembros/$', liderListarMiembrosGrupo, name="listar_miembros"),  # No se usa actualmente
    url(r'^editar_miembros/$', liderEditarMiembros, name="editar_miembros"),  # No se usa actualmente
    url(r'^editar_miembro/(\d+)/$', editarMiembro, name="editar_miembro"),
    url(r'^transladar_miembros/(?P<id_miembro>\d+)$', transladar_miembros, name="transladar_miembros"),  # No se usa actualmente
    # url(r'^editar_perfil/$', liderEditarPerfil, name="editar_perfil"),
    url(r'^editar_perfil/$', RedirectView.as_view(url='/miembro/perfil/')),
    url(r'^perfil/(?P<pk>\d*)$', liderEditarPerfil, name="editar_perfil"),
    url(r'^cambiar_contrasena/$', cambiarContrasena, name="cambiar_contrasena"),
    url(r'^llamadas_pendientes/lider/$', liderLlamadasPendientesVisitantesGrupo, name="llamadas_pendientes_lider"),
    url(r'^llamadas_pendientes/agente/$', llamadasPendientesVisitantes, name="llamadas_pendientes_agente"),  # aqui
    url(r'^registrar_llamada/lider/$', liderLlamarVisitas, name="registrar_llamada_lider"),
    url(r'^registrar_llamada/agente/$', llamarVisitas, name="registrar_llamada_agente"),
    url(r'^promover_visitantes/$', liderPromoverVisitantesGrupo, name="promover_visitantes"),
    url(r'^grupo/(?P<pk>\d*)$', editarHorarioReunionGrupo, name="editar_grupo"),
    url(r'^editar_grupo/$', RedirectView.as_view(url="/miembro/grupo/")),
    url(r'^reportar_reunion_grupo/$', reportarReunionGrupo, name="reportar_reunion_grupo"),  # revisada
    url(r'^reportar_reunion_grupo_admin/$', reportarReunionGrupoAdmin, name="reportar_reunion_grupo_admin"),  # revisada
    # url(r'^perfil/(\d+)/$',  perfilMiembro, name="perfil"),
    url(r'^reportar_reunion_discipulado/$', reportarReunionDiscipulado, name="reportar_reunion_discipulado"),
    url(r'^asignar_grupo/(\d+)/$', asignarGrupo, name="asignar_grupo"),
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
    url(r'^cambiar_tipo_miembro/(\d+)/$', cambiarMiembroDeTipoMiembro, name="cambiar_tipo_miembro"),
    url(r'^detalles_llamada/$', views.listarDetallesLlamada, name="detalles_llamada"),  # revisada
    url(r'^agregar_detalle_llamada/$', views.AgregarDetalleLlamada, name="agregar_detalle_llamada"),  # revisada
    url(r'^editar_detalle_llamada/(?P<pk>\d+)$', views.editarDetalleLlamada, name="editar_detalle_llamada"),  # revisada
    url(r'^graduar_alumno/$', views.graduarAlumno, name="graduar_alumno"),  # revisada
    url(r'^asignar_usuario/(\d+)/$', crearUsuarioMimembro, name="asignar_grupo"),
    url(r'^eliminar_cambio_tipo/(\d+)/$', eliminarCambioTipoMiembro, name="eliminar_cambio_tipo"),  # No usada
    url(r'^cumplimiento_pasos/$', views.cumplimientoPasos, name="cumplimiento_pasos"),  # revisada
    url(r'^discipulos/(?P<pk>\d*)$', ver_discipulos, name="ver_discipulos"),
    url(r'^informacion_iglesia/(?P<pk>\d*)$', ver_informacion_miembro, name="ver_informacion"),
    url(r'^eliminar_foto_perfil/(?P<pk>\d*)$', eliminar_foto_perfil, name="eliminar_foto"),

    url(r'^redes/(?P<pk>\d+)/lideres/$', views.listar_lideres, name='listar_lideres')
]
