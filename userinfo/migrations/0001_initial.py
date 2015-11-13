# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('isbn_number', models.CharField(max_length=500)),
                ('long_term_rent', models.BooleanField(default=False)),
                ('short_term_rent', models.BooleanField(default=False)),
                ('for_buy', models.BooleanField(default=False)),
                ('book_condition', models.CharField(max_length=25)),
                ('for_trade', models.BooleanField(default=False)),
                ('need_investment', models.BooleanField(default=False)),
                ('author', models.CharField(max_length=500)),
                ('price', models.FloatField(default=0.0)),
                ('publish_date', models.DateTimeField(default=datetime.datetime.now, db_index=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.CharField(max_length=100)),
                ('book_image', models.FileField(upload_to=b'image/%Y/%m/%d', verbose_name=b'book image')),
                ('book', models.ForeignKey(default=b'', to='userinfo.Book')),
            ],
        ),
        migrations.CreateModel(
            name='EludeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('college_attending', models.CharField(max_length=254)),
                ('user_books', models.ForeignKey(default=b'', to='userinfo.Book')),
                ('username', models.OneToOneField(default=b'', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MerchantGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to='userinfo.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='NonStudentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to='userinfo.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to='userinfo.EludeUser')),
            ],
        ),
    ]
