# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0004_auto_20160114_0420'),
    ]

    operations = [
        migrations.AddField(
            model_name='soldbooks',
            name='delivered_to_buyer',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='newtransactionprocess',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='soldbooks',
            name='time_book_was_sold',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
