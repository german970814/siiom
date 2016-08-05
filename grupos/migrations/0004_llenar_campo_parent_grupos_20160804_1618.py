# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def listaLideres(grupo, CambioTipo):

    lideres = []
    if grupo.lider1:
        lideres.append(grupo.lider1.id)
        if CambioTipo.objects.filter(miembro=grupo.lider1.conyugue, nuevoTipo__nombre__iexact='lider').exists():
            lideres.append(grupo.lider1.conyugue.id)
    if grupo.lider2:
        lideres.append(grupo.lider2.id)
        if CambioTipo.objects.filter(miembro=grupo.lider2.conyugue, nuevoTipo__nombre__iexact='lider').exists():
            lideres.append(grupo.lider2.conyugue.id)
    return lideres


def llenar_parent_grupos(apps, schema_editor):
    Grupo = apps.get_model("grupos", "Grupo")
    Miembro = apps.get_model("miembros", "Miembro")
    CambioTipo = apps.get_model("miembros", "CambioTipo")

    for grupo in Grupo.objects.all():
        lideres_id = listaLideres(grupo, CambioTipo)

        for lider in Miembro.objects.filter(id__in=lideres_id):
            padre = lider.grupo
            if padre:
                grupo.parent = padre
                grupo.save()
                break


class Migration(migrations.Migration):

    dependencies = [
        ('grupos', '0003_grupo_parent'),
        ('miembros', '0013_auto_20160616_1632'),
    ]

    operations = [
        migrations.RunPython(llenar_parent_grupos, reverse_code=migrations.RunPython.noop)
    ]
