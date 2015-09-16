# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0007_auto_20150915_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='admin',
            field=models.ForeignKey(to='tbs.UserProfile', related_name='notifications_as_admin'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(to='tbs.UserProfile', related_name='notifications_as_user'),
        ),
    ]
