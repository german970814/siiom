from django.conf.urls import include, patterns, url
from .views import *
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
    url(r'^pasos_totales/$', PasosTotales, name="pasos_totales"),
    url(r'^pasos_rango_fechas/$', PasosRangoFecha, name="pasos_rango_fechas"),
    url(r'^estadistico_reunionesGAR/$', estadistico_reuniones_gar, name="estadistico_reunionesGAR"),
    url(r'^cumplimiento_llamadas_lideres/$', cumplimiento_llamadas_lideres_red, name='cumplimiento_llamadas_lideres'),
    url(r'^reportes_reuniones_sin_enviar/$', ConsultarReportesSinEnviar, {}, name="reportes_reuniones_sin_enviar"),
    url(r'^estadistico_reunionesDiscipulado/$',
        estadisticoReunionesDiscipulado, name="estadistico_reunionesDiscipulado"),
    url(r'^estadistico__totalizado_reunionesGAR/$',
        estadisticoTotalizadoReunionesGar, name="estadistico__totalizado_reunionesGAR"),
    url(r'^estadistico__totalizado_reunionesDiscipulado/$',
        estadisticoTotalizadoReunionesDiscipulado, name="estadistico__totalizado_reunionesDiscipulado"),
    url(r'^reportes_reuniones_discipulado_sin_enviar/$',
        ConsultarReportesDiscipuladoSinEnviar, {},
        name="reportes_reuniones_discipulado_sin_enviar"),  # No asignado aun a ningun menu
    url(r'^consultar_sobres_sin_enviar/$',
        ConsultarReportesSinEnviar, {'sobres': True}, name="consultar_sobres_sin_enviar"),  # Error
    url(r'^consultar_sobres_discipulados_sin_enviar/$',
        ConsultarReportesDiscipuladoSinEnviar, {'sobres': True},
        name="consultar_sobres_discipulados_sin_enviar"),  # Error
    # url(r'^prueba/', estadistico_reuniones_gar, name="rueba2")
]
