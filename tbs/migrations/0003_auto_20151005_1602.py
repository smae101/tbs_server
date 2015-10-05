# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0002_auto_20151003_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='date_approved',
            field=models.DateTimeField(null=True, verbose_name='Date Approved', blank=True),
        ),
    ]
