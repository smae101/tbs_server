# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tbs', '0003_auto_20160128_1757'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='stars_based_on_price',
            new_name='rate_of_added_stars_based_on_price',
        ),
        migrations.RenameField(
            model_name='rate',
            old_name='stars_based_on_stars_required',
            new_name='rate_of_added_stars_based_on_stars_required',
        ),
    ]
