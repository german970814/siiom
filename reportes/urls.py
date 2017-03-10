from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^estadistico_reunionesGAR/$', views.estadistico_reuniones_gar, name="estadistico_reuniones_grupo"),
    url(r'^estadistico_reunionesDiscipulado/$',
        views.estadistico_reuniones_discipulado, name="estadistico_reuniones_discipulado"),
    url(r'^estadistico_totalizado_reunionesGAR/$',
        views.estadistico_totalizado_reuniones_gar, name="estadistico_totalizado_reuniones_grupo"),
    url(r'^estadistico_totalizado_reunionesDiscipulado/$',
        views.estadistico_totalizado_reuniones_discipulado, name="estadistico_totalizado_reuniones_discipulado"),
    url(r'^confirmar_ofrenda_grupos_red/$', views.confirmar_ofrenda_grupos_red, name="confirmar_ofrenda_grupos_red"),
]
