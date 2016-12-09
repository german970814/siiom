from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^areas_departamento_json/$', views.areas_departamento_json, name="areas_departamento_json"),
    url(r'^crear_area/$', views.AreaCreateView.as_view(), name="crear_area"),
    url(r'^editar_area/(?P<pk>\d+)$', views.AreaUpdateView.as_view(), name="editar_area"),
    url(r'^listar_areas/$', views.ListaAreasView.as_view(), name="listar_areas"),
    url(r'^crear_departamento/$', views.DepartamentoCreateView.as_view(), name="crear_departamento"),
    url(r'^editar_departamento/(?P<pk>\d+)$', views.DepartamentoUpdateView.as_view(), name="editar_departamento"),
    url(r'^listar_departamentos/$', views.ListaDepartamentosView.as_view(), name="listar_departamentos"),
    url(r'^crear_empleado/$', views.crear_empleado, name="crear_empleado"),
    url(r'^editar_empleado/(?P<id_empleado>\d+)$', views.editar_empleado, name="editar_empleado"),
    url(r'^listar_empleados/$', views.ListaEmpleadosView.as_view(), name="listar_empleados"),

    url(r'^empleados/nuevo/$', views.crear_empleado2, name="empleado_nuevo"),
]
