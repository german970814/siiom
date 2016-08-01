from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^nueva/$', views.crear_requisicion, name="crear_requisicion"),
    url(r'^mis_requisiciones/$', views.ver_requisiciones_empleado, name="ver_requisiciones_empleado"),
    url(r'^editar_requisicion/(?P<id_requisicion>\d+)$', views.editar_requisicion, name="editar_requisicion"),
]
