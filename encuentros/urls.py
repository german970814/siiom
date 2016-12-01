from django.conf.urls import url
from . import views, api

urlpatterns = [
    url(r'^nuevo/$', views.crear_encuentro, name="crear_encuetro"),  # revisada
    url(r'^encuentros/$', views.listar_encuentros, name="listar_encuentros"),  # revisada
    url(r'^agregar_encontrista/(?P<id_encuentro>\d+)/$', views.agregar_encontrista, name="agregar_encontrista"),  # revisada
    url(r'^editar_encuentro/(?P<id_encuentro>\d+)/$', views.editar_encuentro, name="editar_encuentro"),  # revisada
    url(r'^listar_encontristas/(?P<id_encuentro>\d+)/$', views.listar_encontristas, name="listar_encontristas"),  # revisada
    url(r'^editar_encontrista/(?P<id_encontrista>\d+)/$', views.editar_encontrista, name="editar_encontrista"),  # revisada
    url(r'^borrar_encontrista/(?P<id_encontrista>\d+)/$', views.borrar_encontrista, name="borrar_encontrista"),  # revisada
    url(r'^asistencia_encuentro/(?P<id_encuentro>\d+)/$', views.asistencia_encuentro, name="asistencia_encuentro"),  # revisada
    url(r'^obtener_grupos/$', api.obtener_grupos, name="obtener_grupos"),  # revisada
    url(
        r'^obtener_coordinadores_tesoreros/$',
        api.obtener_coordinadores_tesoreros,
        name="obtener_coordinadores_tesoreros"
    ),  # revisada
]
