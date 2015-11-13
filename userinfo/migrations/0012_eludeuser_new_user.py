# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0011_auto_20151003_0713'),
    ]

    operations = [
        migrations.AddField(
            model_name='eludeuser',
            name='new_user',
            field=models.BooleanField(default=False),
        ),
    ]
