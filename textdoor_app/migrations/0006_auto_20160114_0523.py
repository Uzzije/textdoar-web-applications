# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0005_auto_20160114_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateTimeField(default=django.utils.timezone.now, db_index=True, blank=True),
        ),
        migrations.AlterField(
            model_name='newtransactionprocess',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='paymentcarddata',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='soldbooks',
            name='time_book_was_sold',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
