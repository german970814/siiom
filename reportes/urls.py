from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^miembros_y_pasos/$', views.pasosPorMiembros, name="miembros_y_pasos"),
    url(r'^pasos_totales/$', views.PasosTotales, name="pasos_totales"),
    url(r'^pasos_rango_fechas/$', views.PasosRangoFecha, name="pasos_rango_fechas"),
    url(r'^estadistico_reunionesGAR/$', views.estadistico_reuniones_gar, name="estadistico_reunionesGAR"),
    url(r'^estadistico_reunionesDiscipulado/$',
        views.estadisticoReunionesDiscipulado, name="estadistico_reunionesDiscipulado"),
    url(r'^estadistico__totalizado_reunionesGAR/$',
        views.estadisticoTotalizadoReunionesGar, name="estadistico__totalizado_reunionesGAR"),
    url(r'^estadistico__totalizado_reunionesDiscipulado/$',
        views.estadisticoTotalizadoReunionesDiscipulado, name="estadistico__totalizado_reunionesDiscipulado"),
    url(r'^confirmar_ofrenda_grupos_red/$', views.confirmar_ofrenda_grupos_red, name="confirmar_ofrenda_grupos_red"),
]
