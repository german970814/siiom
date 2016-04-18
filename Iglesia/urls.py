from django.conf.urls import include, patterns, url
from django.views.generic import RedirectView
from django.contrib import admin
from miembros.views import autenticarUsario, salir, administracion, recuperar_contrasena
from views import resultadoBusqueda, depu, depu2, without_perms
import os
from django.conf import settings
admin.autodiscover()
RedirectView.permanent = True
handler404 = 'views.custom_404'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url="/iniciar_sesion/")),
    url(r'^iniciar_sesion/$', autenticarUsario, name="inicio"),
    url(r'^administracion/$',  administracion, name="administracion"),
    url(r'^salir/$', salir),
    url(r'^resultado/(grupo|miembro)/$',  resultadoBusqueda),
    url(r'^miembro/', include("miembros.urls")),
    url(r'^grupo/', include("grupos.urls")),
    url(r'^reportes/', include("reportes.urls")),
    url(r'^recuperar_contrasena/$', recuperar_contrasena, name='recuperar_contrasena'),
    url(r'^dont_have_permissions/$', without_perms, name="sin_permiso"),
    # url(r'^grupo/reportes_reuniones_sin_enviar/$', ConsultarReportesSinEnviar),
    # url(r'^grupo/consultar_sobres_sin_enviar/$', ConsultarSobresSinEnviar),
)

urlpatterns += patterns('',
    #  --------------------------AMBOS------------------------
    url(r'^academia/',  include("academia.urls")),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
    )
