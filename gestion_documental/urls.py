from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ingresar_registro/$', views.ingresar_registro, name="ingresar_registro"),
    url(r'^busqueda_registros/$', views.busqueda_registros, name="busqueda_registros"),
    url(r'^palabras_claves_json/$', views.palabras_claves_json, name="palabras_claves_json"),
    url(r'^area_tipo_documento_json/$', views.area_tipo_documento_json, name="area_tipo_documento_json"),
]
