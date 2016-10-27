from django.conf.urls import include, patterns, url
from .views import *

urlpatterns = [
    url(r'^asignar_grupo_visitas/$', asignar_grupo_visitas, name="asignar_grupo_visitas"),
    url(r'^visitas/nueva/$', CrearVisita.as_view(), name="crear_visita"),
    url(r'^visitas/editar/(?P<pk>\d+)/$', EditarVisita.as_view(), name="editar_visita"),
    url(r'^/api/visitas/asignar/$', asignar_grupo_visitas_ajax, name="asignar_grupo_visitas_ajax"),
]
