from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ingresar_registro/$', views.ingresar_registro, name="ingresar_registro"),
    url(r'^busqueda_registros/$', views.busqueda_registros, name="busqueda_registros"),
    url(r'^palabras_claves_json/$', views.palabras_claves_json, name="palabras_claves_json"),
    url(r'^area_tipo_documento_json/$', views.area_tipo_documento_json, name="area_tipo_documento_json"),
    url(r'^crear_tipo_documento/$', views.TipoDocumentoCreateView.as_view(), name="crear_tipo_documento"),
    url(r'^editar_tipo_documento/(?P<pk>\d+)$', views.TipoDocumentoUpdateView.as_view(), name="editar_tipo_documento"),
    url(r'^crear_palabra_clave/$', views.PalabraClaveCreateView.as_view(), name="crear_palabra_clave"),
    url(r'^editar_palabra_clave/(?P<pk>\d+)$', views.PalabraClaveUpdateView.as_view(), name="editar_palabra_clave"),
    url(r'^listar_tipo_documentos/$', views.ListaTipoDocumentosView.as_view(), name="listar_tipo_documentos"),
    url(r'^listar_palabras_claves/$', views.ListaPalabrasClavesView.as_view(), name="listar_palabras_claves"),
]
