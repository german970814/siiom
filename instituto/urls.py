from django.conf.urls import url
from . import views, api

urlpatterns = [
    # url(r'^/$', views.lista_estudiantes_sesion, name="a"),
    url(r'^materias/$', views.MateriaListView.as_view(), name='materias'),
    url(r'^materias/new/$', views.MateriaCreateView.as_view(), name='crear-materia'),
    url(r'^materias/(?P<pk>\d+)/$', views.MateriaUpdateView.as_view(), name='editar-materia'),
    url(r'^modulos/(?P<materia_pk>\d+)/$', views.ModuloListView.as_view(), name='modulos'),
    url(r'^modulos/(?P<materia_pk>\d+)/new/$', views.ModuloCreateView.as_view(), name='crear-modulo'),
    url(r'^modulos/(?P<pk>\d+)/edit/$', views.ModuloUpdateView.as_view(), name='editar-modulo'),
    url(r'^sesiones/(?P<modulo_pk>\d+)/$', views.SesionListView.as_view(), name='sesiones'),
    url(r'^sesiones/(?P<modulo_pk>\d+)/new/$', views.SesionCreateView.as_view(), name='crear-sesion'),
    url(r'^sesiones/(?P<pk>\d+)/edit/$', views.SesionUpdateView.as_view(), name='editar-sesion'),
    url(r'^salones/$', views.SalonListView.as_view(), name='salones'),
    url(r'^salones/new/$', views.SalonCreateView.as_view(), name='crear-salon'),
    url(r'^salones/(?P<pk>\d+)/edit/$', views.SalonUpdateView.as_view(), name='editar-salon'),
    url(r'^cursos/$', views.CursoCreateView.as_view(), name="crear-curso"),
    url(r'^reporte_instituto/$', views.reporte_instituto, name="reporte-instituto"),
    url(r'^api/cursos/salon/(?P<pk>\d+)/$', api.curso_by_month, name="api-cursos-salon"),
    url(r'^api/cursos/salon/(?P<pk>\d+)/disponibilidad/$', api.verifica_disponibilidad_curso, name="api-disponibilidad-cursos-salon"),
]
