# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miembros', '0024_auto_20170307_1609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='miembro',
            old_name='estadoCivil',
            new_name='estado_civil',
        ),
        migrations.RenameField(
            model_name='miembro',
            old_name='fechaNacimiento',
            new_name='fecha_nacimiento',
        ),
        migrations.RenameField(
            model_name='miembro',
            old_name='fechaRegistro',
            new_name='fecha_registro',
        ),
        migrations.RenameField(
            model_name='miembro',
            old_name='primerApellido',
            new_name='primer_apellido',
        ),
        migrations.RenameField(
            model_name='miembro',
            old_name='segundoApellido',
            new_name='segundo_apellido',
        ),
    ]
