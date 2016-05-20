# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def eliminar_usuario_no_asignados_a_miembros(apps, schema_editor):
    """Elimina los usuarios que no han sido asignados a ningún miembro exceptuando los usuarios que tienen como
    username un email de algún miembro."""

    Miembro = apps.get_model('miembros', 'Miembro')
    User = apps.get_model('auth', 'User')

    lista_emails = Miembro.objects.values_list('email', flat=True)
    usuarios = User.objects.filter(miembro=None).exclude(username__in=lista_emails)
    usuarios.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0008_auto_20160430_1039'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.RunPython(eliminar_usuario_no_asignados_a_miembros),
    ]
