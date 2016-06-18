from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ingresar_registro/$', views.ingresar_registro, name="ingresar_registro"),
    url(r'^api/$', views.api, name="api"),
]
