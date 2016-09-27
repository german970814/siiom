# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.db.models import Q


def grupo_lidera(miembro, Grupo):
    try:
        if miembro.conyugue:
            return Grupo.objects.get(
                Q(lider1=miembro) | Q(lider1=miembro.conyugue) | Q(lider2=miembro) | Q(lider2=miembro.conyugue)
            )
        else:
            return Grupo.objects.get(Q(lider1=miembro) | Q(lider2=miembro))
    except:
        return None


def llenar_grupo_lidera(apps, schema_editor):
    Miembro = apps.get_model("miembros", "Miembro")
    Grupo = apps.get_model("grupos", "Grupo")

    for miembro in Miembro.objects.all():
        grupo = grupo_lidera(miembro, Grupo)

        if grupo:
            miembro.grupo_lidera = grupo
            miembro.save()


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0014_miembro_grupo_lidera'),
        ('grupos', '0006_llenar_grupo_parent_20160927_1747'),
    ]

    operations = [
        migrations.RunPython(llenar_grupo_lidera, reverse_code=migrations.RunPython.noop)
    ]
