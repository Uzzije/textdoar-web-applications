# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0010_auto_20160119_0438'),
    ]

    operations = [
        migrations.CreateModel(
            name='LaunchPageEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_email', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
    ]
