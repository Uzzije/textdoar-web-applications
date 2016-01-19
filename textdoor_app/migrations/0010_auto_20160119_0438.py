# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0009_soldbooks_order_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentfeedbacks',
            name='email',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='studentfeedbacks',
            name='topic',
            field=models.CharField(max_length=36, null=True, blank=True),
        ),
    ]
