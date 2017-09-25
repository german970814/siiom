from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/$', views.lista_estudiantes_sesion, name="a"),
    url(r'^reporte_instituto/$', views.reporte_instituto, name="reporte_instituto"),
]
