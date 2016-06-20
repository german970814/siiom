from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^areas_departamento_json/$', views.areas_departamento_json, name="areas_departamento_json"),
]
