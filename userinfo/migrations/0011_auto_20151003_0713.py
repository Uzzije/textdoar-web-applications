# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0010_bookrentedout_bookstradingout_bookyouarerenting_bookyoubought_bookyouinvestin_bookyousold_yourbookth'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookTradingOut',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_received', models.DateTimeField(default=None, verbose_name=b'Time book was received')),
                ('additional_information', models.TextField(verbose_name=b'Additional Information about book trade i.e length of trade')),
                ('length_of_trade', models.CharField(default=b'None', max_length=250, verbose_name=b'Length of trade')),
                ('has_book_been_returned', models.BooleanField(default=False, verbose_name=b'Has book been Returned')),
                ('item_traded_for_if_not_book', models.CharField(default=None, max_length=250, verbose_name=b'Item traded for, if not book')),
                ('time_book_was_traded', models.DateTimeField(default=None, verbose_name=b'Time book was traded out')),
                ('price', models.CharField(default=None, max_length=250)),
                ('book', models.ForeignKey(related_name='your_book', to='userinfo.Book')),
                ('book_gotten_in_trade', models.ForeignKey(related_name='book_gotten_in_trade', to='userinfo.Book')),
                ('user', models.ForeignKey(to='userinfo.EludeUser')),
            ],
        ),
        migrations.RemoveField(
            model_name='bookstradingout',
            name='book',
        ),
        migrations.RemoveField(
            model_name='bookstradingout',
            name='book_gotten_in_trade',
        ),
        migrations.RemoveField(
            model_name='bookstradingout',
            name='user',
        ),
        migrations.DeleteModel(
            name='BooksTradingOut',
        ),
    ]
