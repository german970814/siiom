from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^asignar_grupo_visitas/$', views.asignar_grupo_visitas, name="asignar_grupo_visitas"),  # revisada
    url(r'^visitas/nueva/$', views.CrearVisita.as_view(), name="crear_visita"),  # revisada
    url(r'^visitas/editar/(?P<pk>\d+)/$', views.EditarVisita.as_view(), name="editar_visita"),  # revisada
    url(r'^/api/visitas/asignar/$', views.asignar_grupo_visitas_ajax, name="asignar_grupo_visitas_ajax"),  # revisada
]
