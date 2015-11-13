# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0008_auto_20150919_2336'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.ForeignKey(default=b'No order history', to='userinfo.Book')),
                ('user', models.ForeignKey(to='userinfo.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='RepGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to='userinfo.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.ForeignKey(default=b'No book on watch list', to='userinfo.Book')),
                ('user', models.ForeignKey(to='userinfo.EludeUser')),
            ],
        ),
    ]
