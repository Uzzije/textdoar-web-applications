# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0005_auto_20151129_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
    ]
