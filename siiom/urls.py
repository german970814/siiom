import views

from django.conf.urls import include, patterns, url
from django.views.generic import RedirectView
from django.contrib import admin
from django.conf import settings
from miembros.views import login, logout, administracion, recuperar_contrasena

admin.autodiscover()
RedirectView.permanent = True

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url="/iniciar_sesion/")),
    url(r'^iniciar_sesion/$', login, name="inicio"),
    url(r'^salir/$', logout, name='logout'),
    url(r'^administracion/$', administracion, name="administracion"),
    url(r'^miembro/', include("miembros.urls", namespace='miembros')),
    url(r'^grupo/', include("grupos.urls", namespace='grupos')),
    url(r'^reportes/', include("reportes.urls", namespace='reportes')),
    url(r'^encuentro/', include("encuentros.urls", namespace='encuentros')),
    url(r'^consolidacion/', include("consolidacion.urls", namespace="consolidacion")),
    url(r'^common/', include("common.urls", namespace="common")),
    url(r'^recuperar_contrasena/$', recuperar_contrasena, name='recuperar_contrasena'),
    url(r'^dont_have_permissions/$', views.without_perms, name="sin_permiso"),

    url(r'^organizacional/', include("organizacional.urls", namespace="organizacional")),
    url(r'^requisiciones/', include("compras.urls", namespace="compras")),
    url(r'^sgd/', include("gestion_documental.urls", namespace="sgd")),
    url(r'^pqr/', include("pqr.urls", namespace="pqr")),

    url(r'^buscar/(grupo|miembro)/$', views.buscar, name='buscar')
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
    )
    try:
        import debug_toolbar
        urlpatterns += patterns(
            '',
            url(r'^__debug__/', include(debug_toolbar.urls)),
        )
    except ImportError:
        pass