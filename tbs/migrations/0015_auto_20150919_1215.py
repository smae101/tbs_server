# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0014_notification_maker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='target',
            field=models.ForeignKey(related_name='target', to=settings.AUTH_USER_MODEL),
        ),
    ]
