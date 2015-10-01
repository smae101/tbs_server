# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0016_auto_20150922_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='date_approved',
            field=models.DateTimeField(verbose_name='Date Approved', null=True),
        ),
    ]
