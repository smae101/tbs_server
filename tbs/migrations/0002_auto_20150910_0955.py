# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='first_name',
            field=models.CharField(default='Sheila Mae', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='last_name',
            field=models.CharField(default='Batistil', max_length=255),
            preserve_default=False,
        ),
    ]
