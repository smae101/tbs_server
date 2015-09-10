# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import tbs.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalDonateRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('request_expiration', models.DateTimeField(default=tbs.models.ApprovalDonateRequest.expiry)),
                ('donor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalSellRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('request_expiration', models.DateTimeField(default=tbs.models.ApprovalSellRequest.expiry)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('category_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('status', models.CharField(choices=[('reserved', 'Reserved'), ('available', 'Available')], max_length=15)),
                ('purpose', models.CharField(choices=[('sell', 'Sell'), ('donate', 'Donate')], max_length=10)),
                ('price', models.FloatField()),
                ('picture', models.URLField()),
                ('stars_required', models.IntegerField()),
                ('category', models.ForeignKey(to='tbs.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('message', models.CharField(max_length=500)),
                ('notification_type', models.CharField(choices=[('sell', 'Sell'), ('buy', 'Buy'), ('donate', 'Donate')], max_length=10)),
                ('status', models.CharField(choices=[('read', 'Read'), ('unread', 'Unread')], max_length=10)),
                ('admin', models.ForeignKey(related_name='admin', to=settings.AUTH_USER_MODEL)),
                ('item', models.OneToOneField(to='tbs.Item')),
                ('user', models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReservationRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('reserved_date', models.DateTimeField()),
                ('request_expiration', models.DateTimeField()),
                ('status', models.CharField(max_length=10)),
                ('buyer', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('item', models.OneToOneField(to='tbs.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('id_number', models.CharField(max_length=20)),
                ('course', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date_claimed', models.DateTimeField()),
                ('buyer', models.ForeignKey(related_name='transactions_as_buyer', to=settings.AUTH_USER_MODEL)),
                ('item', models.OneToOneField(to='tbs.Item')),
                ('owner', models.ForeignKey(related_name='transactions_as_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('stars_collected', models.IntegerField(default=0)),
                ('student', models.OneToOneField(to='tbs.Student')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(to='tbs.Student'),
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
