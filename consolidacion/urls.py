from django.conf.urls import include, patterns, url
from .views import *

urlpatterns = [
    url(r'^asignar_grupo_visitas/$', asignar_grupo_visitas, name="asignar_grupo_visitas"),
]
