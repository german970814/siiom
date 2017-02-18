from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^api/buscar_miembro/(?P<pk>\d+)/$', api.busqueda_miembro_api, name="busqueda_miembro_api"),
    url(r'^api/buscar_grupo/(?P<pk>\d+)/$', api.busqueda_grupo_api, name="busqueda_grupo_api"),
]
