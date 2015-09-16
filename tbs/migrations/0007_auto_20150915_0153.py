# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0006_auto_20150915_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='admin',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='admin'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='item',
            field=models.ForeignKey(to='tbs.Item'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='user'),
        ),
    ]
