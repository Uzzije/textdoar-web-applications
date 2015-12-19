# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listedbookforsale',
            name='make_it_availiable',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 29, 6, 23, 25, 70575)),
        ),
    ]
