# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0002_auto_20150910_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='stars_required',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(max_length=10, default='unread', choices=[('read', 'Read'), ('unread', 'Unread')]),
        ),
    ]
