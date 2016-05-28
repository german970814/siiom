from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^nuevo/$', views.crear_encuentro, name="crear_encuetro"),
    url(r'^encuentros/$', views.listar_encuentros, name="listar_encuentros"),
    url(r'^agregar_encontrista/(?P<id_encuentro>\d+)/$', views.agregar_encontrista, name="agregar_encontrista"),
    url(r'^listar_encontristas/(?P<id_encuentro>\d+)/$', views.listar_encontristas, name="listar_encontristas"),
    url(r'^editar_encontrista/(?P<id_encontrista>\d+)/$', views.editar_encontrista, name="editar_encontrista"),
    url(r'^borrar_encontrista/(?P<id_encontrista>\d+)/$', views.borrar_encontrista, name="borrar_encontrista"),
    url(r'^asistencia_encuentro/(?P<id_encuentro>\d+)/$', views.asistencia_encuentro, name="asistencia_encuentro"),
    url(r'^obtener_grupos/$', views.obtener_grupos, name="obtener_grupos"),
]
