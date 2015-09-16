# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0008_auto_20150915_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='user',
            new_name='target',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='admin',
        ),
    ]
