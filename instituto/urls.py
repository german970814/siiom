from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^/$', views.lista_estudiantes_sesion, name="a"),
    url(r'^materia/$', views.MateriaListView.as_view(), name='materias'),
    url(r'^materia/new/$', views.MateriaCreateView.as_view(), name='crear-materia'),
    url(r'^materia/(?P<pk>\d+)/$', views.MateriaUpdateView.as_view(), name='editar-materia'),
    url(r'^modulo/(?P<materia_pk>\d+)/$', views.ModuloListView.as_view(), name='modulos'),
    url(r'^modulo/(?P<materia_pk>\d+)/new/$', views.ModuloCreateView.as_view(), name='crear-modulo'),
    url(r'^modulo/(?P<pk>\d+)/edit/$', views.ModuloUpdateView.as_view(), name='editar-modulo'),
    url(r'^sesion/(?P<modulo_pk>\d+)/$', views.SesionListView.as_view(), name='sesiones'),
    url(r'^sesion/(?P<modulo_pk>\d+)/new/$', views.SesionCreateView.as_view(), name='crear-sesion'),
    url(r'^sesion/(?P<pk>\d+)/edit/$', views.SesionUpdateView.as_view(), name='editar-sesion'),
    url(r'^salon/$', views.SalonListView.as_view(), name='salones'),
    url(r'^salon/new/$', views.SalonCreateView.as_view(), name='crear-salon'),
    url(r'^salon/(?P<pk>\d+)/edit/$', views.SalonUpdateView.as_view(), name='editar-salon'),
    url(r'^reporte_instituto/$', views.reporte_instituto, name="reporte_instituto"),
]
