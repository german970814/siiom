from django.conf.urls import include, patterns, url
from .views import *

urlpatterns = [
	url(r'^visitas_por_red/$', visitasAsignadasRedes, name="visitas_por_red"),
    url(r'^asignacion_gar/$', asignacionGAR, name="asignacion_gar"),
    url(r'^primera_llamada/$', detalleLlamada, {'llamada': 1}, name="primera_llamada"),
    url(r'^segunda_llamada/$', detalleLlamada, {'llamada': 2}, name="segunda_llamada"),
    url(r'^visitas_por_mes/$', visitasPorMes, {'por_red': False}, name="visitas_por_mes"),
    url(r'^visitas_red_por_mes/$', visitasPorMes, {'por_red': True}, name="visitas_red_por_mes"),
    url(r'^asistencia_reuniones/$', asistenciaGrupos, name="asistencia_reuniones"),
    url(r'^miembros_y_pasos/$', pasosPorMiembros, name="miembros_y_pasos"),
    url(r'^pasos_totales/$', PasosTotales, name="pasos_totales"),
    url(r'^pasos_rango_fechas/$', PasosRangoFecha, name="pasos_rango_fechas"),
    url(r'^estadistico_reunionesGAR/$', estadisticoReunionesGar, name="estadistico_reunionesGAR"),
    url(r'^estadistico_reunionesDiscipulado/$', estadisticoReunionesDiscipulado, name="estadistico_reunionesDiscipulado"),
    url(r'^estadistico__totalizado_reunionesGAR/$', estadisticoTotalizadoReunionesGar, name="estadistico__totalizado_reunionesGAR"),
    url(r'^estadistico__totalizado_reunionesDiscipulado/$', estadisticoTotalizadoReunionesDiscipulado, name="estadistico__totalizado_reunionesDiscipulado"),
    url(r'^desarrollo_grupos/$', desarrolloGrupo, name="desarrollo_grupos"),
    url(r'^reportes_reuniones_sin_enviar/$', ConsultarReportesSinEnviar, {}, name="reportes_reuniones_sin_enviar"),
    url(r'^reportes_reuniones_discipulado_sin_enviar/$', ConsultarReportesDiscipuladoSinEnviar, {}, name="reportes_reuniones_discipulado_sin_enviar"),
    url(r'^consultar_sobres_sin_enviar/$', ConsultarReportesSinEnviar, {'sobres': True}, name="consultar_sobres_sin_enviar"),
    url(r'^consultar_sobres_discipulados_sin_enviar/$', ConsultarReportesDiscipuladoSinEnviar, {'sobres': True}, name="consultar_sobres_discipulados_sin_enviar"),
    url(r'^reportes/cumplimiento_llamadas_lideres/$', cumplimiento_llamadas_lideres_red, name='cumplimiento_llamadas_lideres'),
]