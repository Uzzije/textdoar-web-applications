# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0002_auto_20151121_2139'),
    ]

    operations = [
        migrations.CreateModel(
            name='EludeUserAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(default=None, max_length=600)),
                ('city', models.CharField(default=None, max_length=600)),
                ('state', models.CharField(default=None, max_length=600)),
                ('zip_code', models.CharField(default=None, max_length=600)),
            ],
        ),
        migrations.AddField(
            model_name='eludeuser',
            name='address',
            field=models.ManyToManyField(to='textdoor_app.EludeUserAddress'),
        ),
    ]
