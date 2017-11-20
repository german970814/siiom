from django.conf.urls import url
from . import views
from . import api

urlpatterns = [
    url(r'^$', views.nuevo_caso, name="nuevo_caso"),
    url(r'^sc/$', views.nuevo_caso_servicio_cliente, name="nuevo_caso_servicio_cliente"),
    url(r'^casos/$', views.ver_casos_servicio_cliente, name="ver_casos_servicio_cliente"),
    url(r'^caso/(?P<id_caso>\d+)/$', views.ver_bitacora_caso, name="ver_bitacora_caso"),
    url(r'^editar/(?P<id_caso>\d+)/$', views.editar_caso, name="editar_caso"),
    url(r'^casos/empleado/$', views.ver_casos_empleado, name="ver_casos_empleado"),
    url(r'^casos/comercial/$', views.ver_casos_jefe_comercial, name="ver_casos_jefe_comercial"),
    url(r'^casos/presidencia/$', views.ver_casos_presidencia, name="ver_casos_presidencia"),
    url(r'^download/file/(?P<id_documento>\d+)/$', views.descargar_archivos, name="descargar_archivos"),
    url(r'^upload/file/(?P<id_caso>\d+)/$', views.subir_archivo_como_bitacora, name="subir_archivo_como_bitacora"),
    url(r'^api/empleados/(?P<id_caso>\d+)/$', api.empleados_nombres_views, name="empleados_nombres_views_api"),
]
