# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def actualiza_tesoreros_coordinadores(apps, schema_editor):
    Encuentro = apps.get_model('encuentros', 'Encuentro')
    Group = apps.get_model('auth', 'Group')
    try:
        Tesorero = Group.objects.get(name__icontains='tesorero')
        Coordinador = Group.objects.get(name__icontains='coordinador')
        for encuentro in Encuentro.objects.all():
            if encuentro.estado == 'A':
                if not encuentro.tesorero.usuario.groups.filter(name__icontains='tesorero').exists():
                    encuentro.tesorero.usuario.groups.add(Tesorero)
                if not encuentro.coordinador.usuario.groups.filter(name__icontains='coordinador').exists():
                    encuentro.coordinador.usuario.groups.add(Coordinador)
    except:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('encuentros', '0002_auto_20170405_1756'),
    ]

    operations = [
        migrations.RunPython(actualiza_tesoreros_coordinadores),
    ]
