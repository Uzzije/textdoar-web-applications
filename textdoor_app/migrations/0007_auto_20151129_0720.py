# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0006_auto_20151129_0710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='eight_weeks_rent_price',
            field=models.CharField(default=b'0.00', max_length=500),
        ),
        migrations.AlterField(
            model_name='book',
            name='rent_price',
            field=models.CharField(default=b'0.00', max_length=500),
        ),
        migrations.AlterField(
            model_name='book',
            name='sales_price',
            field=models.CharField(default=b'0.00', max_length=500),
        ),
        migrations.AlterField(
            model_name='book',
            name='short_term_rent_price',
            field=models.CharField(default=b'0.00', max_length=500),
        ),
    ]
