# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0007_booksstudentsrequested_studentfeedbacks'),
    ]

    operations = [
        migrations.AddField(
            model_name='booksstudentsrequested',
            name='email',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
