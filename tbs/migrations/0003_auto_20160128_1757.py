# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0002_auto_20160123_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('tbs_share', models.IntegerField(default=0)),
                ('user_share', models.IntegerField(default=0)),
                ('penalty_rate_per_day', models.IntegerField(default=0)),
                ('stars_based_on_price', models.IntegerField(default=0)),
                ('stars_based_on_stars_required', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='reserved_quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='tbs_share',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='total_payment',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='user_share',
            field=models.FloatField(default=0),
        ),
    ]
