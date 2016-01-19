# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0006_auto_20160114_0523'),
    ]

    operations = [
        migrations.CreateModel(
            name='BooksStudentsRequested',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_of_book', models.CharField(max_length=100, blank=True)),
                ('isbn_number', models.CharField(max_length=100, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentFeedBacks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('feed_back', models.CharField(max_length=2000, blank=True)),
                ('email', models.CharField(max_length=30, blank=True)),
                ('topic', models.CharField(max_length=36, blank=True)),
            ],
        ),
    ]
