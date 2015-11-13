# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0009_orderhistory_repgroup_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookRentedOut',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_received', models.DateTimeField(verbose_name=b'Time book was received')),
                ('additional_information', models.TextField(verbose_name=b'Additional Information about book rental i.e length of rent')),
                ('time_book_was_rented_out', models.DateTimeField(verbose_name=b'Time book was rented out')),
                ('has_book_been_returned', models.BooleanField(default=False, verbose_name=b'Has book been Returned')),
                ('type_of_rent', models.CharField(default=None, max_length=250, verbose_name=b"Length of Book's Rent")),
                ('price', models.CharField(default=None, max_length=250)),
                ('book', models.ForeignKey(to='userinfo.Book')),
                ('user', models.ForeignKey(to='userinfo.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='BooksTradingOut',
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
        migrations.CreateModel(
            name='BookYouAreRenting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_received', models.DateTimeField(verbose_name=b'Time renting began')),
                ('additional_information', models.TextField(verbose_name=b'Additional Information about book rental i.e length of rent')),
                ('time_book_was_rented_out', models.DateTimeField(verbose_name=b'Time renting ended or should end')),
                ('has_book_been_returned', models.BooleanField(default=False, verbose_name=b'Has book been Returned to owner?')),
                ('type_of_rent', models.CharField(default=b'None', max_length=250, verbose_name=b"Length of Book's Rent")),
                ('price', models.CharField(default=None, max_length=250)),
                ('book', models.ForeignKey(to='userinfo.Book')),
                ('user', models.ForeignKey(to='userinfo.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='BookYouBought',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('additional_information', models.TextField(verbose_name=b'Additional Information about book rental i.e length of rent')),
                ('time_book_was_bought', models.DateTimeField(verbose_name=b'Time book was bought')),
                ('price', models.CharField(default=None, max_length=250)),
                ('book', models.ForeignKey(to='userinfo.Book')),
                ('user', models.ForeignKey(to='userinfo.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='BookYouInvestIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_invested_in', models.CharField(default=None, max_length=250, verbose_name=b'Amount invested in book')),
                ('additional_information', models.TextField(default=None, verbose_name=b'Additional information')),
                ('price', models.CharField(default=None, max_length=250)),
                ('book_invested_in', models.ForeignKey(to='userinfo.Book')),
                ('investors', models.ManyToManyField(related_name='investors', to='userinfo.EludeUser')),
                ('user_invested_in', models.ForeignKey(related_name='user_i_am_investing_in', to='userinfo.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='BookYouSold',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('additional_information', models.TextField(verbose_name=b'Additional Information about book sold')),
                ('time_book_was_sold', models.DateTimeField(verbose_name=b'Time book was sold')),
                ('price', models.CharField(default=None, max_length=250)),
                ('book', models.ForeignKey(to='userinfo.Book')),
                ('user', models.ForeignKey(to='userinfo.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='YourBookThatWasInvestedIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount_invested_in_your_book', models.CharField(default=None, max_length=250, verbose_name=b'Amount invested in book')),
                ('additional_information', models.TextField(default=None, verbose_name=b'Additional information')),
                ('price', models.CharField(default=None, max_length=250)),
                ('book_invested_in', models.ForeignKey(to='userinfo.Book')),
                ('investors', models.ManyToManyField(to='userinfo.EludeUser')),
            ],
        ),
    ]
