# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tbs.models
import unixtimestampfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvaldonaterequest',
            name='request_date',
            field=unixtimestampfield.fields.UnixTimeStampField(default=tbs.models.ApprovalDonateRequest.date_now),
        ),
        migrations.AlterField(
            model_name='approvaldonaterequest',
            name='request_expiration',
            field=unixtimestampfield.fields.UnixTimeStampField(default=tbs.models.ApprovalDonateRequest.expiry),
        ),
        migrations.AlterField(
            model_name='approvalsellrequest',
            name='request_date',
            field=unixtimestampfield.fields.UnixTimeStampField(default=tbs.models.ApprovalSellRequest.date_now),
        ),
        migrations.AlterField(
            model_name='approvalsellrequest',
            name='request_expiration',
            field=unixtimestampfield.fields.UnixTimeStampField(default=tbs.models.ApprovalSellRequest.expiry),
        ),
        migrations.AlterField(
            model_name='item',
            name='date_approved',
            field=unixtimestampfield.fields.UnixTimeStampField(default=0.0),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_date',
            field=unixtimestampfield.fields.UnixTimeStampField(default=tbs.models.Notification.date_now),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_expiration',
            field=unixtimestampfield.fields.UnixTimeStampField(default=tbs.models.Notification.expiry),
        ),
        migrations.AlterField(
            model_name='reservationrequest',
            name='request_expiration',
            field=unixtimestampfield.fields.UnixTimeStampField(default=tbs.models.ReservationRequest.expiry),
        ),
        migrations.AlterField(
            model_name='reservationrequest',
            name='reserved_date',
            field=unixtimestampfield.fields.UnixTimeStampField(default=tbs.models.ReservationRequest.date_now),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date_claimed',
            field=unixtimestampfield.fields.UnixTimeStampField(default=0.0),
        ),
    ]
