from django.conf.urls import url
from . import api

urlpatterns = [
    url(r'^api/buscar_miembro/(?P<pk>\d+)/$', api.busqueda_miembro_api, name="busqueda_miembro_api"),
]
