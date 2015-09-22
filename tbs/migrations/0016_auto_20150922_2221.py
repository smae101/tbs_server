# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tbs.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0015_auto_20150919_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvaldonaterequest',
            name='donor',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='approvalsellrequest',
            name='seller',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, to='tbs.Category', null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='item',
            name='purpose',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='notification',
            name='maker',
            field=models.ForeignKey(default='admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='notification',
            name='status',
            field=models.CharField(max_length=10, default='unread'),
        ),
        migrations.AlterField(
            model_name='reservationrequest',
            name='buyer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reservationrequest',
            name='request_expiration',
            field=models.DateTimeField(default=tbs.models.ReservationRequest.expiry),
        ),
        migrations.AlterField(
            model_name='reservationrequest',
            name='reserved_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
