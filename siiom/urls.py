import views

from django.conf.urls import include, patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from django.contrib import admin
from django.conf import settings
from miembros.views import login, logout, administracion
from miembros import forms as miembros_forms

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
    url(r'^dont_have_permissions/$', views.without_perms, name="sin_permiso"),

    url(r'^organizacional/', include("organizacional.urls", namespace="organizacional")),
    url(r'^requisiciones/', include("compras.urls", namespace="compras")),
    url(r'^sgd/', include("gestion_documental.urls", namespace="sgd")),
    url(r'^pqr/', include("pqr.urls", namespace="pqr")),

    url(r'^buscar/(grupo|miembro)/$', views.buscar, name='buscar'),
    url(
        r'^recuperar_contrasena/$', auth_views.password_reset,
        {
            'subject_template_name': 'miembros/contrasena/email_subject.html',
            'template_name': 'miembros/contrasena/password_reset_form.html',
            'email_template_name': 'miembros/contrasena/email_body.html',
            'password_reset_form': miembros_forms.PasswordResetForm,
        },
        name="recuperar_contrasena"
    ),
    url(
        r'^recuperar_contrasena/enviado/$', auth_views.password_reset_done,
        {
            'template_name': 'miembros/contrasena/password_reset_done.html'
        },
        name="password_reset_done"),
    url(
        r'^resetear_contrasena/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {
            'template_name': 'miembros/contrasena/password_reset_confirm.html',
            'set_password_form': miembros_forms.SetPasswordForm
        },
        name="password_reset_confirm"
    ),
    url(
        r'^resetear_contrasena/done/$',
        auth_views.password_reset_complete,
        {'template_name': 'miembros/contrasena/password_reset_complete.html'},
        name="password_reset_complete"
    ),
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
