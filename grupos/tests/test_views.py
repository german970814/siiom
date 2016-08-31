from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, Group
from miembros.models import Miembro
from .base import GruposBaseTest


class DesarrolloGrupoViewTest(GruposBaseTest):
    """
    Prueba la vista de desarrollo de grupos.
    """

    def ingresar_pagina(self, login=True):
        """Ingresa a la página de desarrollo de grupos y retorna el reponse. Por defecto loguea al usuario."""

        if login:
            self.login_usuario()
        return self.client.get(reverse('grupos:desarrollo_grupos'))

    def test_usuario_no_logueado_redireccionado_login(self):
        """Prueba que un usuario no logueado sea redireccionado al login."""

        response = self.ingresar_pagina(login=False)
        self.assertRedirects(response, reverse('inicio'))


    def test_usuario_logueado_no_lider_ni_admin_redireccionado_sin_permisos(self):
        """Prueba que un usuario logueado que no sea administrador ni líder sea redireccionado a página que indique que
        no tiene permisos."""

        response = self.ingresar_pagina()
        self.assertRedirects(response, reverse('sin_permiso'))

    def test_admin_vea_arbol_grupos_completo(self):
        """Prueba que un administrador pueda ver el arbol completo de la iglesia."""

        self.usuario.user_permissions.add(Permission.objects.get(codename='es_administrador'))
        response = self.ingresar_pagina()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grupos/desarrollo_grupo.html')
        self.assertListEqual(response.context['arbol'], self.lista_arbol_completo)

    def test_lider_vea_arbol_desde_grupo_lidera(self):
        """Prueba que un líder solo pueda ver el arbol desde su grupo hacia abajo."""

        self.usuario.user_permissions.add(Permission.objects.get(codename='es_lider'))
        miembro = Grupo.objects.get(id=3).lider1
        miembro.usuario = self.usuario
        miembro.save()

        response = self.ingresar_pagina()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grupos/desarrollo_grupo.html')
        self.assertListEqual(response.context['arbol'], self.lista_arbol_cb2)
