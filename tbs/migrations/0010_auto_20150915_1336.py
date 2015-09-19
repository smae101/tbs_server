# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0009_auto_20150915_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(related_name='owner', to='tbs.UserProfile'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='target',
            field=models.ForeignKey(related_name='target', to='tbs.UserProfile'),
        ),
    ]
