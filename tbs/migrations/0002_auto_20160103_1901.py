# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='renteditem',
            name='penalty',
            field=models.FloatField(default=0),
        ),
    ]
