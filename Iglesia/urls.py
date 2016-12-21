import views

from django.conf.urls import include, patterns, url
from django.views.generic import RedirectView
from django.contrib import admin
from django.conf import settings
from miembros.views import autenticarUsario, salir, administracion, recuperar_contrasena

admin.autodiscover()
RedirectView.permanent = True
handler404 = 'views.custom_404'

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url="/iniciar_sesion/")),
    url(r'^iniciar_sesion/$', autenticarUsario, name="inicio"),  # revisada
    url(r'^administracion/$', administracion, name="administracion"),  # revisada
    url(r'^salir/$', salir),  # revisada
    url(r'^miembro/', include("miembros.urls", namespace='miembros')),  # revisada
    url(r'^grupo/', include("grupos.urls", namespace='grupos')),  # revisada
    url(r'^academia/', include("academia.urls", namespace='academia')),  # revisada
    url(r'^reportes/', include("reportes.urls", namespace='reportes')),  # revisada
    url(r'^encuentro/', include("encuentros.urls", namespace='encuentros')),  # revisada
    url(r'^consolidacion/', include("consolidacion.urls", namespace="consolidacion")),  # revisada
    url(r'^common/', include("common.urls", namespace="common")),
    url(r'^recuperar_contrasena/$', recuperar_contrasena, name='recuperar_contrasena'),  # revisada
    url(r'^dont_have_permissions/$', views.without_perms, name="sin_permiso"),  # revisada

    url(r'^organizacional/', include("organizacional.urls", namespace="organizacional")),  # revisada
    url(r'^requisiciones/', include("compras.urls", namespace="compras")),
    url(r'^sgd/', include("gestion_documental.urls", namespace="sgd")),  # revisada
    url(r'^pqr/', include("pqr.urls", namespace="pqr")),

    url(r'^buscar/(grupo|miembro)/$', views.buscar, name='buscar')
    # url(r'^mapa/$', views.mapa, name="mapa"),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
    )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
