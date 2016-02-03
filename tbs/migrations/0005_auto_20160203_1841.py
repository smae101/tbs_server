# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0004_auto_20160128_1906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='item',
        ),
        migrations.AddField(
            model_name='transaction',
            name='item_name',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='buyer',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='seller',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]
