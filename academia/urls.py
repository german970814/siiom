from django.conf.urls import include, patterns, url
from .views import *
from miembros.views import administracion

urlpatterns = [
	#  --------------------------AMBOS------------------------
    url(r'^curso_detalle/(\d+)/$', verDetalleCurso, name="curso_detalle"),
    url(r'^estudiantes/(\d+)/$', listarEstudiantes, name="estudiantes"),
    url(r'^estudiante_detalle/(\d+)/$', verDetalleEstudiante, name="estudiante_detalle"),
    #  ---------------------------MAESTRO---------------------
    url(r'^cursos/$',  verCursos, {'admin': False}, name="cursos"),
    url(r'^editar_curso/(?P<pk>\d+)$',  editarCurso, {'admin': False, 'url': '/cursos/'}, name="editar_curso"),
    url(r'^asistencia/$',  maestroAsistencia, name="asistencia"),
    url(r'^evaluar_modulo/$',  evaluarModulo, name="evaluar_modulo"),
    url(r'^registrar_entrega_tarea/$',  maestroRegistrarEntregaTareas, name="registrar_entrega_tarea"),
    url(r'^promover_estudiante/$',  promoverModulo, name="promover_estudiante"),
    #  ----------------ADMINISTRADOR-----------------------
    url(r'^crear_curso/$',  crearCurso, name="crear_curso"),
    url(r'^listar_cursos/$',  verCursos, {'admin': True}, name="listar_cursos"),
    url(r'^admin_editar_curso/(?P<pk>\d+)$',  editarCurso, {'admin': True, 'url': '/listar_cursos/'}, name="admin_editar_curso"),
    url(r'^matricular/(\d+)/$',  matricularEstudiante, name="matricular"),
    url(r'^crear_modulo/$',  crearModulo, name="crear_modulo"),
    url(r'^listar_modulos/$',  listarModulos, name="listar_modulos"),
    url(r'^editar_modulo/(?P<pk>\d+)$', editarModulo, name='editar_modulo'),
    url(r'^crear_sesion/(\d+)/$',  crearSesion, name="editar_sesion"),
    url(r'^sesiones/(\d+)/$',  listarSesiones, name="sesiones"),
    url(r'^editar_sesion/(?P<id>\d+)/(?P<pk>\d+)$',  editarSesion, name="editar_sesion"),
    url(r'^listar_pagos/$',  listarPagosAcademia, name="listar_pagos"),

    #  ----------------RECEPTOR-----------------------
    url(r'^recibir_pago/(\d+)/$',  recibirPago, name="recibir_pago"),
]
