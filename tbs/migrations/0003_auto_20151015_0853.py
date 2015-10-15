# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tbs.models


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0002_remove_item_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discounted_price',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='notification',
            name='notification_expiration',
            field=models.DateTimeField(default=tbs.models.Notification.expiry),
        ),
    ]
