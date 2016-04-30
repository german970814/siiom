# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


def agregar_email_miembros(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    for user in User.objects.all():
        user.email = user.username
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0007_auto_20160429_1032'),
    ]

    operations = [
        migrations.RunPython(agregar_email_miembros, reverse_code=migrations.RunPython.noop),
    ]
