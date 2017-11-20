from django.conf.urls import url
from . import views, api

urlpatterns = [
    url(r'^nueva/$', views.crear_requisicion, name="crear_requisicion"),
    url(r'^mis_requisiciones/$', views.ver_requisiciones_empleado, name="ver_requisiciones_empleado"),
    url(r'^editar_requisicion/(?P<id_requisicion>\d+)/$', views.editar_requisicion, name="editar_requisicion"),
    url(r'^requisiciones_compras/$', views.ver_requisiciones_compras, name="ver_requisiciones_compras"),
    url(r'^pago_requisicion/(?P<id_requisicion>\d+)/$', views.pre_pago_requisicion, name="pre_pago_requisicion"),
    url(r'^pago/(?P<id_requisicion>\d+)/$', views.pagar_requisicion, name="pagar_requisicion"),
    url(r'^requisiciones_usuario_pago/$', views.ver_requisiciones_usuario_pago, name="ver_requisiciones_usuario_pago"),
    url(r'^proveedor/$', views.listar_proveedores, name="listar_proveedores"),
    url(r'^proveedor/nuevo/$', views.crear_proveedor, name="crear_proveedor"),
    url(r'^proveedor/editar/(?P<id_proveedor>\d+)/$', views.editar_proveedor, name="editar_proveedor"),
    url(
        r'^empleado/aprobar_requisicion/(?P<id_requisicion>\d+)/$',
        views.aprobar_requisiciones_empleado, name="aprobar_requisiciones_empleado"
    ),
    url(
        r'^editar_requisicion_jefe_administrativo/(?P<id_requisicion>\d+)/$',
        views.editar_valores_jefe_administrativo,
        name="editar_valores_jefe_administrativo"
    ),
    url(
        r'^adjuntar/(?P<id_requisicion>\d+)/$',
        views.adjuntar_archivos_requisicion,
        name="adjuntar_archivos_requisicion"
    ),
    url(
        r'^requisiciones_jefe_departamento/$',
        views.ver_requisiciones_jefe_departamento,
        name="ver_requisiciones_jefe_departamento"
    ),
    url(
        r'^requisiciones_jefe_administrativo/$',
        views.ver_requisiciones_jefe_administrativo,
        name="ver_requisiciones_jefe_administrativo"
    ),
    url(
        r'^requisiciones_presidencia/$',
        views.ver_requisiciones_presidencia,
        name="ver_requisiciones_presidencia"
    ),
    url(
        r'^requisiciones_financiero/$',
        views.ver_requisiciones_financiero,
        name="ver_requisiciones_financiero"
    ),
    url(
        r'^api/detalles/(?P<id_requisicion>\d+)/$',
        api.detalles_requisicion_api,
        name="detalles_requisicion_api"
    ),
    url(
        r'^api/observaciones/(?P<id_requisicion>\d+)/$',
        api.observaciones_requisicion,
        name="observaciones_requisicion"
    ),
    url(
        r'^api/comentada/(?P<id_requisicion>\d+)/$',
        api.requisicion_comentada_api,
        name="requisicion_comentada_api"
    ),
    url(
        r'^api/comentada_compras/(?P<id_requisicion>\d+)/$',
        api.requisicion_comentada_compras_api,
        name="requisicion_comentada_compras_api"
    ),
    url(
        r'^api/comentada_jefe_administrativo/(?P<id_requisicion>\d+)/$',
        api.requisicion_comentada_jefe_administrativo_api,
        name="requisicion_comentada_jefe_administrativo_api"
    ),
    url(
        r'^api/comentada_presidencia/(?P<id_requisicion>\d+)/$',
        api.requisicion_comentada_presidencia_api,
        name="requisicion_comentada_presidencia_api"
    ),
    url(
        r'^api/descargar_archivos_api/(?P<id_archivo>\d+)/$',
        api.descargar_archivos_api,
        name="descargar_archivos_api"
    ),
    url(
        r'^api/get_areas/(?P<id_departamento>\d+)/$',
        api.get_areas_by_departamento_json,
        name="get_areas_by_departamento_json"
    ),
    url(
        r'^informes/totales/$',
        views.informes_totales_area_departamento,
        name="informes_totales_area_departamento"
    ),
    url(
        r'^imprimir/(?P<id_requisicion>\d+)/$',
        views.imprimir_requisicion,
        name="imprimir_requisicion"
    ),
]
