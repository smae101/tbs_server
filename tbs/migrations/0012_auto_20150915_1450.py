# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0011_auto_20150915_1448'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='owner',
            new_name='seller',
        ),
    ]
