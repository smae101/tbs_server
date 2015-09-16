# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0012_auto_20150915_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvaldonaterequest',
            name='donor',
            field=models.ForeignKey(to='tbs.UserProfile'),
        ),
        migrations.AlterField(
            model_name='approvalsellrequest',
            name='seller',
            field=models.ForeignKey(to='tbs.UserProfile'),
        ),
        migrations.AlterField(
            model_name='reservationrequest',
            name='buyer',
            field=models.ForeignKey(to='tbs.UserProfile'),
        ),
    ]
