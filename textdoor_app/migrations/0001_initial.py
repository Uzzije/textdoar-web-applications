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
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='BookImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.CharField(max_length=100)),
                ('book_image', models.ImageField(upload_to=b'image/%Y/%m/%d', verbose_name=b'book image')),
                ('book', models.ForeignKey(default=b'', to='textdoor_app.Book')),
            ],
        ),
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
                ('book', models.ForeignKey(to='textdoor_app.Book')),
            ],
        ),
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
                ('book', models.ForeignKey(related_name='your_book', to='textdoor_app.Book')),
                ('book_gotten_in_trade', models.ForeignKey(related_name='book_gotten_in_trade', to='textdoor_app.Book')),
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
                ('book', models.ForeignKey(to='textdoor_app.Book')),
            ],
        ),
        migrations.CreateModel(
            name='BookYouBought',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('additional_information', models.TextField(verbose_name=b'Additional Information about book rental i.e length of rent')),
                ('time_book_was_bought', models.DateTimeField(verbose_name=b'Time book was bought')),
                ('price', models.CharField(default=None, max_length=250)),
                ('book', models.ForeignKey(to='textdoor_app.Book')),
            ],
        ),
        migrations.CreateModel(
            name='BookYouSold',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('additional_information', models.TextField(verbose_name=b'Additional Information about book sold')),
                ('time_book_was_sold', models.DateTimeField(verbose_name=b'Time book was sold')),
                ('price', models.CharField(default=None, max_length=250)),
                ('book', models.ForeignKey(to='textdoor_app.Book')),
            ],
        ),
        migrations.CreateModel(
            name='EludeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('college_attending', models.CharField(max_length=254)),
                ('new_user', models.BooleanField(default=True)),
                ('username', models.OneToOneField(default=b'', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MerchantGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to='textdoor_app.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='NewTransactionProcess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('at_least_one_book_sold', models.BooleanField(default=False, verbose_name=b'Check if user bought at least a textbook')),
                ('book', models.ManyToManyField(to='textdoor_app.Book')),
                ('user', models.ForeignKey(default=b'guest', to='textdoor_app.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='NonStudentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to='textdoor_app.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.ForeignKey(default=b'No order history', to='textdoor_app.Book')),
                ('user', models.ForeignKey(to='textdoor_app.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='RepGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to='textdoor_app.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='StudentGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to='textdoor_app.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.ForeignKey(default=b'No book on watch list', to='textdoor_app.Book')),
                ('user', models.ForeignKey(to='textdoor_app.EludeUser')),
            ],
        ),
        migrations.AddField(
            model_name='bookyousold',
            name='user',
            field=models.ForeignKey(to='textdoor_app.EludeUser'),
        ),
        migrations.AddField(
            model_name='bookyoubought',
            name='user',
            field=models.ForeignKey(to='textdoor_app.EludeUser'),
        ),
        migrations.AddField(
            model_name='bookyouarerenting',
            name='user',
            field=models.ForeignKey(to='textdoor_app.EludeUser'),
        ),
        migrations.AddField(
            model_name='booktradingout',
            name='user',
            field=models.ForeignKey(to='textdoor_app.EludeUser'),
        ),
        migrations.AddField(
            model_name='bookrentedout',
            name='user',
            field=models.ForeignKey(to='textdoor_app.EludeUser'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_owner',
            field=models.ForeignKey(default=b'', to='textdoor_app.EludeUser'),
        ),
    ]
