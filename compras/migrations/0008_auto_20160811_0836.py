# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compras', '0007_auto_20160810_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parametros',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dias_habiles', models.PositiveSmallIntegerField(verbose_name='dias hábiles')),
                ('tope_monto', models.PositiveIntegerField(verbose_name='monto tope para presidencia')),
            ],
        ),
        migrations.AddField(
            model_name='requisicion',
            name='presupuesto_aprobado',
            field=models.CharField(verbose_name='presupuesto aprobado', choices=[('SI', 'SI'), ('ES', 'EN ESPERA')], max_length=1, blank=True),
        ),
    ]
