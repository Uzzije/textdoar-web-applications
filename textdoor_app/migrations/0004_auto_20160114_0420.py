# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0003_auto_20160112_0156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasedbooks',
            name='book',
        ),
        migrations.RemoveField(
            model_name='purchasedbooks',
            name='user',
        ),
        migrations.RemoveField(
            model_name='soldbooks',
            name='user',
        ),
        migrations.AddField(
            model_name='book',
            name='book_is_sold',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='soldbooks',
            name='buyer',
            field=models.ForeignKey(related_name='buyer', blank=True, to='textdoor_app.EludeUser', null=True),
        ),
        migrations.AddField(
            model_name='soldbooks',
            name='seller',
            field=models.ForeignKey(related_name='seller', blank=True, to='textdoor_app.EludeUser', null=True),
        ),
        migrations.AlterField(
            model_name='eludeuseraddress',
            name='current_shipping_address',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='soldbooks',
            name='time_book_was_sold',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.DeleteModel(
            name='PurchasedBooks',
        ),
    ]
