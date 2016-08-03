from django.conf.urls import url
from . import views, api

urlpatterns = [
    url(r'^nueva/$', views.crear_requisicion, name="crear_requisicion"),
    url(r'^mis_requisiciones/$', views.ver_requisiciones_empleado, name="ver_requisiciones_empleado"),
    url(r'^editar_requisicion/(?P<id_requisicion>\d+)$', views.editar_requisicion, name="editar_requisicion"),
    url(r'^compras/$', views.ver_requisiciones_compras, name="ver_requisiciones_compras"),
    url(
        r'^adjuntar/(?P<id_requisicion>\d+)$',
        views.adjuntar_archivos_requisicion,
        name="adjuntar_archivos_requisicion"
    ),
    url(
        r'^requisiciones/$',
        views.ver_requisiciones_jefe_departamento,
        name="ver_requisiciones_jefe_departamento"
    ),
    url(
        r'^api/detalles/(?P<id_requisicion>\d+)$',
        api.detalles_requisicion_api,
        name="detalles_requisicion_api"
    ),
    url(
        r'^api/observaciones/(?P<id_requisicion>\d+)$',
        api.observaciones_requisicion,
        name="observaciones_requisicion"
    ),
    url(
        r'^api/comentada/(?P<id_requisicion>\d+)$',
        api.requisicion_comentada_api,
        name="requisicion_comentada_api"
    ),
]
