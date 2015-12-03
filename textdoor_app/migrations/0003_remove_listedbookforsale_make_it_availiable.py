# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0002_listedbookforsale_make_it_availiable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listedbookforsale',
            name='make_it_availiable',
        ),
    ]
