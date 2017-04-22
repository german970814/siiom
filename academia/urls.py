from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^curso_detalle/(\d+)/$', views.verDetalleCurso, name="curso_detalle"),  # revisada
    url(r'^estudiantes/(\d+)/$', views.listarEstudiantes, name="estudiantes"),  # revisada
    url(r'^estudiante_detalle/(\d+)/$', views.verDetalleEstudiante, name="estudiante_detalle"),  # revisada
    url(r'^editar_modulo/(?P<pk>\d+)$', views.editarModulo, name='editar_modulo'),  # revisada
    url(r'^mis-cursos/$', views.verCursos, {'admin': False}, name="mis_cursos"),  # revisada
    url(r'^listar_cursos/$', views.verCursos, {'admin': True}, name="listar_cursos"),  # revisada
    url(r'^cursos/$', views.verCursos, {'admin': True}, name="cursos"),  # revisada
    url(r'^editar_curso/(?P<pk>\d+)$', views.editarCurso, {'admin': False, 'url': '/cursos/'}, name="editar_curso"),  # revisada
    url(r'^asistencia/$', views.maestroAsistencia, name="asistencia"),  # revisada
    url(r'^evaluar_modulo/$', views.evaluarModulo, name="evaluar_modulo"),  # revisada
    url(r'^registrar_entrega_tarea/$', views.maestroRegistrarEntregaTareas, name="registrar_entrega_tarea"),  # revisada
    url(r'^promover_estudiante/$', views.promoverModulo, name="promover_estudiante"),  # revisada
    url(r'^crear_curso/$', views.crearCurso, name="crear_curso"),  # revisada
    url(r'^matricular/(\d+)/$', views.matricularEstudiante, name="matricular"),  # revisada
    url(r'^crear_modulo/$', views.crearModulo, name="crear_modulo"),  # revisada
    url(r'^listar_modulos/$', views.listarModulos, name="listar_modulos"),  # revisada
    url(r'^crear_sesion/(\d+)/$', views.crearSesion, name="crear_sesion"),  # revisada
    url(r'^sesiones/(\d+)/$', views.listarSesiones, name="sesiones"),  # revisada
    url(r'^editar_sesion/(?P<id>\d+)/(?P<pk>\d+)$', views.editarSesion, name="editar_sesion"),  # revisada
    url(r'^listar_pagos/$', views.listarPagosAcademia, name="listar_pagos"),  # revisada
    url(r'^recibir_pago/(\d+)/$', views.recibirPago, name="recibir_pago"),  # revisada
    url(r'^admin_editar_curso/(?P<pk>\d+)$',
        views.editarCurso, {'admin': True, 'url': '/listar_cursos/'}, name="admin_editar_curso"),  # revisada
]
