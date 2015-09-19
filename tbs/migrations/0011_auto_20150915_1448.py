# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0010_auto_20150915_1336'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ('-date_claimed',)},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='buyer',
            field=models.ForeignKey(to='tbs.UserProfile', related_name='transactions_as_buyer'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='owner',
            field=models.ForeignKey(to='tbs.UserProfile', related_name='transactions_as_owner'),
        ),
    ]
