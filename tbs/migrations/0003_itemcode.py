# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0002_auto_20160106_0818'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCode',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('item_code', models.CharField(default='0', max_length=100)),
            ],
        ),
    ]
