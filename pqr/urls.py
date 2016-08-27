from django.conf.urls import url
from . import views
from . import api

urlpatterns = [
    url(r'^$', views.nuevo_caso, name="nuevo_caso"),
    # url(r'^festivos/$', views.definir_festivos, name="definir_festivos"),
    url(r'^validar_email/(?P<llave>.+)$', views.validar_caso, name="validar_caso"),
    url(r'^casos/$', views.ver_casos_servicio_cliente, name="ver_casos_servicio_cliente"),
    url(r'^caso/(?P<id_caso>\d+)$', views.ver_bitacora_caso, name="ver_bitacora_caso"),
    url(r'^casos/empleado/$', views.ver_casos_empleado, name="ver_casos_empleado"),
    url(r'^casos/comercial/$', views.ver_casos_jefe_comercial, name="ver_casos_jefe_comercial"),
    url(r'^api/empleados/(?P<id_caso>\d+)$', api.empleados_nombres_views, name="empleados_nombres_views_api"),
]
