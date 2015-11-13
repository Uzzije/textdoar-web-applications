# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0012_eludeuser_new_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eludeuser',
            name='new_user',
            field=models.BooleanField(default=True),
        ),
    ]
