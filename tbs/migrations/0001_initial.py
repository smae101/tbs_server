# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tbs.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalDonateRequest',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('request_expiration', models.DateTimeField(default=tbs.models.ApprovalDonateRequest.expiry)),
                ('donor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalSellRequest',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('request_expiration', models.DateTimeField(default=tbs.models.ApprovalSellRequest.expiry)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('category_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('status', models.CharField(max_length=15)),
                ('purpose', models.CharField(max_length=10)),
                ('price', models.FloatField(default=0)),
                ('picture', models.URLField()),
                ('stars_required', models.IntegerField(default=0)),
                ('date_approved', models.DateTimeField(verbose_name='Date Approved', null=True)),
                ('category', models.ForeignKey(to='tbs.Category', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('message', models.CharField(max_length=500)),
                ('notification_type', models.CharField(max_length=10)),
                ('status', models.CharField(default='unread', max_length=10)),
                ('notification_date', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(to='tbs.Item')),
                ('maker', models.ForeignKey(default='admin', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='target')),
            ],
        ),
        migrations.CreateModel(
            name='ReservationRequest',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('reserved_date', models.DateTimeField(auto_now_add=True)),
                ('request_expiration', models.DateTimeField(default=tbs.models.ReservationRequest.expiry)),
                ('status', models.CharField(max_length=10)),
                ('buyer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('item', models.OneToOneField(to='tbs.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('id_number', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('course', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date_claimed', models.DateTimeField()),
            ],
            options={
                'ordering': ('-date_claimed',),
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('stars_collected', models.IntegerField(default=0)),
                ('student', models.OneToOneField(to='tbs.Student')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='buyer',
            field=models.ForeignKey(to='tbs.UserProfile', related_name='transactions_as_buyer'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='item',
            field=models.OneToOneField(to='tbs.Item'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='seller',
            field=models.ForeignKey(to='tbs.UserProfile', related_name='transactions_as_owner'),
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(to='tbs.UserProfile', related_name='owner'),
        ),
        migrations.AddField(
            model_name='approvalsellrequest',
            name='item',
            field=models.OneToOneField(to='tbs.Item'),
        ),
        migrations.AddField(
            model_name='approvalsellrequest',
            name='seller',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='approvaldonaterequest',
            name='item',
            field=models.OneToOneField(to='tbs.Item'),
        ),
    ]
