# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0008_booksstudentsrequested_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='soldbooks',
            name='order_number',
            field=models.CharField(default=b'00000', max_length=1000),
        ),
    ]
