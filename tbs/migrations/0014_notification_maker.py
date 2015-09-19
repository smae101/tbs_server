# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0013_auto_20150915_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='maker',
            field=models.ForeignKey(default=9, to='tbs.UserProfile'),
            preserve_default=False,
        ),
    ]
