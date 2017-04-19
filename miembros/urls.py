from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views, api, forms
from grupos.views import editar_horario_reunion_grupo


urlpatterns = [
    url(r'^$', views.miembro_inicio, name="miembro_inicio"),
    url(r'^perfil/(?P<pk>\d*)$', views.editar_perfil_miembro, name="editar_perfil"),
    url(r'^cambiar_contrasena/$', views.cambiar_contrasena_miembro, name="cambiar_contrasena"),
    url(r'^grupo/(?P<pk>\d*)$', editar_horario_reunion_grupo, name="editar_grupo"),
    url(r'^asignar_grupo/(\d+)/$', views.asignar_grupo, name="asignar_grupo"),
    url(r'^crear_zona/$', views.crear_zona, name="crear_zona"),
    url(r'^editar_zona/(?P<pk>\d+)$', views.editar_zona, name="editar_zona"),
    url(r'^listar_zonas/$', views.listar_zonas, name="listar_zonas"),
    url(r'^barrios/(\d+)/$', views.barrios_zona, name="barrios"),
    url(r'^crear_barrio/(\d+)/$', views.crear_barrio, name="crear_barrio"),
    url(r'^editar_barrio/(?P<id>\d+)/(?P<pk>\d+)$', views.editar_barrio, name="editar_barrio"),
    url(r'^crear_tipo_miembro/$', views.crear_tipo_miembro, name="crear_tipo_miembro"),
    url(r'^listar_tipo_miembro/$', views.listar_tipos_miembro, name="listar_tipo_miembro"),
    url(r'^editar_tipo_miembro/(?P<pk>\d+)$', views.editar_tipo_miembro, name="editar_tipo_miembro"),
    url(r'^asignar_usuario/(\d+)/$', views.crear_usuario_miembro, name="asignar_usuario"),
    url(r'^eliminar_cambio_tipo/(\d+)/$', views.eliminar_cambio_tipo_miembro, name="eliminar_cambio_tipo"),
    url(r'^discipulos/(?P<pk>\d*)$', views.ver_discipulos, name="ver_discipulos"),
    url(r'^informacion_iglesia/(?P<pk>\d*)$', views.ver_informacion_miembro, name="ver_informacion"),
    url(r'^eliminar_foto_perfil/(?P<pk>\d*)$', views.eliminar_foto_perfil, name="eliminar_foto"),

    url(r'^nuevo/$', views.crear_miembro, name='nuevo'),
    url(r'^(?P<pk>\d+)/trasladar/$', views.trasladar, name='trasladar'),
    url(r'^redes/(?P<pk>\d+)/lideres/$', views.listar_lideres, name='listar_lideres'),
    url(
        r'^cambiar_contrasena2/$', auth_views.password_change,
        {
            'post_change_redirect': 'miembros:miembro_inicio',
            'template_name': 'miembros/cambiar_contrasena2.html',
            'password_change_form': forms.CambiarContrasenaForm
        },
        name="cambiar_contrasena2"
    ),

    url(r'^api/desvincular_lider/(?P<pk>\d+)/$', api.desvincular_lider_grupo_api, name='desvincular_grupo_api'),
]
