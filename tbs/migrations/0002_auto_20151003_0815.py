# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='student',
            name='id_number',
            field=models.CharField(max_length=50),
        ),
    ]
