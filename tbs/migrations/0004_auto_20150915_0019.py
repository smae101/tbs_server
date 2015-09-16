# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0003_auto_20150915_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='stars_required',
            field=models.IntegerField(default=0),
        ),
    ]
