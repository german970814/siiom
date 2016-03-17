from django.conf.urls import include, patterns, url
from .views import *

urlpatterns = [
	url(r'^grupo_padre/$', grupoRaiz, name="grupo_padre"),
    url(r'^(\d+)/$', verGrupo, name="grupo"),
    url(r'^listar_redes/$', listarRedes, name="listar_redes"),
    url(r'^crear_red/$', crearRed, name="crear_red"),
    url(r'^editar_red/(?P<pk>\d+)$', editarRed, name="editar_red"),
    url(r'^listar_grupos/(\d+)/$',  gruposDeRed, name="listar_grupos"),
    url(r'^crear_grupo/(\d+)/$', crearGrupo, name="crear_grupo"),
    url(r'^editar_grupo/$', editarGrupo, name="editar_grupo"),
    url(r'^listar_predicas/$', listarPredicas, name="listar_predicas"),
    url(r'^crear_predica/$', crearPredica, name="crear_predica"),
    url(r'^editar_predica/(?P<pk>\d+)$', editarPredica, name="editar_predica"),
]