from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^visitas_por_red/$', views.visitasAsignadasRedes, name="visitas_por_red"),  # revisada
    url(r'^asignacion_gar/$', views.asignacionGAR, name="asignacion_gar"),  # revisada
    url(r'^primera_llamada/$', views.detalleLlamada, {'llamada': 1}, name="primera_llamada"),  # revisada
    url(r'^segunda_llamada/$', views.detalleLlamada, {'llamada': 2}, name="segunda_llamada"),  # revisada
    url(r'^visitas_por_mes/$', views.visitasPorMes, {'por_red': False}, name="visitas_por_mes"),  # revisada
    url(r'^visitas_red_por_mes/$', views.visitasPorMes, {'por_red': True}, name="visitas_red_por_mes"),  # revisada
    url(r'^asistencia_reuniones/$', views.asistenciaGrupos, name="asistencia_reuniones"),  # revisada la asistencia ya no se lleva
    url(r'^miembros_y_pasos/$', views.pasosPorMiembros, name="miembros_y_pasos"),  # revisada
    url(r'^pasos_totales/$', views.PasosTotales, name="pasos_totales"),  # revisada
    url(r'^pasos_rango_fechas/$', views.PasosRangoFecha, name="pasos_rango_fechas"),  # revisada
    url(r'^estadistico_reunionesGAR/$', views.estadistico_reuniones_gar, name="estadistico_reunionesGAR"),  # revisada
    url(r'^cumplimiento_llamadas_lideres/$', views.cumplimiento_llamadas_lideres_red, name='cumplimiento_llamadas_lideres'),  # revisada
    url(r'^reportes_reuniones_sin_enviar/$', views.ConsultarReportesSinEnviar, {}, name="reportes_reuniones_sin_enviar"),  # revisada
    url(r'^estadistico_reunionesDiscipulado/$',
        views.estadisticoReunionesDiscipulado, name="estadistico_reunionesDiscipulado"),  # revisada
    url(r'^estadistico__totalizado_reunionesGAR/$',
        views.estadisticoTotalizadoReunionesGar, name="estadistico__totalizado_reunionesGAR"),  # revisada
    url(r'^estadistico__totalizado_reunionesDiscipulado/$',
        views.estadisticoTotalizadoReunionesDiscipulado, name="estadistico__totalizado_reunionesDiscipulado"),  # revisada
    url(r'^reportes_reuniones_discipulado_sin_enviar/$',
        views.ConsultarReportesDiscipuladoSinEnviar, {},
        name="reportes_reuniones_discipulado_sin_enviar"),  # No asignado aun a ningun menu revisada
    url(r'^consultar_sobres_sin_enviar/$',
        views.ConsultarReportesSinEnviar, {'sobres': True}, name="consultar_sobres_sin_enviar"),  # Error revisada no usada
    url(r'^consultar_sobres_discipulados_sin_enviar/$',
        views.ConsultarReportesDiscipuladoSinEnviar, {'sobres': True},
        name="consultar_sobres_discipulados_sin_enviar"),  # Error revisada
]
