# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0005_notification_notification_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='admin',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='admin'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='user'),
        ),
    ]
