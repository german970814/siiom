from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^curso_detalle/(\d+)/$', views.verDetalleCurso, name="curso_detalle"),
    url(r'^estudiantes/(\d+)/$', views.listarEstudiantes, name="estudiantes"),
    url(r'^estudiante_detalle/(\d+)/$', views.verDetalleEstudiante, name="estudiante_detalle"),
    url(r'^editar_modulo/(?P<pk>\d+)$', views.editarModulo, name='editar_modulo'),
    url(r'^cursos/$', views.verCursos, {'admin': False}, name="cursos"),
    url(r'^editar_curso/(?P<pk>\d+)$', views.editarCurso, {'admin': False, 'url': '/cursos/'}, name="editar_curso"),
    url(r'^asistencia/$', views.maestroAsistencia, name="asistencia"),
    url(r'^evaluar_modulo/$', views.evaluarModulo, name="evaluar_modulo"),
    url(r'^registrar_entrega_tarea/$', views.maestroRegistrarEntregaTareas, name="registrar_entrega_tarea"),
    url(r'^promover_estudiante/$', views.promoverModulo, name="promover_estudiante"),
    url(r'^crear_curso/$', views.crearCurso, name="crear_curso"),
    url(r'^listar_cursos/$', views.verCursos, {'admin': True}, name="listar_cursos"),
    url(r'^matricular/(\d+)/$', views.matricularEstudiante, name="matricular"),
    url(r'^crear_modulo/$', views.crearModulo, name="crear_modulo"),
    url(r'^listar_modulos/$', views.listarModulos, name="listar_modulos"),
    url(r'^crear_sesion/(\d+)/$', views.crearSesion, name="crear_sesion"),
    url(r'^sesiones/(\d+)/$', views.listarSesiones, name="sesiones"),
    url(r'^editar_sesion/(?P<id>\d+)/(?P<pk>\d+)$', views.editarSesion, name="editar_sesion"),
    url(r'^listar_pagos/$', views.listarPagosAcademia, name="listar_pagos"),
    url(r'^recibir_pago/(\d+)/$', views.recibirPago, name="recibir_pago"),
    url(r'^admin_editar_curso/(?P<pk>\d+)$',
        views.editarCurso, {'admin': True, 'url': '/listar_cursos/'}, name="admin_editar_curso"),
]
