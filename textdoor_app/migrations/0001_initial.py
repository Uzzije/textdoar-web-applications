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
                ('title', models.CharField(max_length=500, db_index=True)),
                ('isbn_number', models.CharField(max_length=500, db_index=True)),
                ('long_term_rent', models.BooleanField(default=False)),
                ('short_term_rent', models.BooleanField(default=False)),
                ('for_buy', models.BooleanField(default=False)),
                ('book_condition', models.CharField(max_length=25)),
                ('need_investment', models.BooleanField(default=False)),
                ('author', models.CharField(max_length=500)),
                ('sales_price', models.FloatField(default=0.0)),
                ('rent_price', models.FloatField(default=0.0)),
                ('short_term_rent_price', models.FloatField(default=0.0)),
                ('eight_weeks_rent_price', models.FloatField(default=0.0)),
                ('publish_date', models.DateTimeField(default=datetime.datetime.now, db_index=True, blank=True)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='BookAcquiredByRent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rented_date', models.DateTimeField(verbose_name=b'Time book was received')),
                ('additional_information', models.TextField(verbose_name=b'Additional Information about book rental i.e length of rent')),
                ('return_date', models.DateTimeField(verbose_name=b'Time book was rented out')),
                ('has_book_been_returned', models.BooleanField(default=False, verbose_name=b'Has book been Returned')),
                ('type_of_rent', models.CharField(default=None, max_length=250, verbose_name=b"Length of Book's Rent")),
                ('book', models.ForeignKey(to='textdoor_app.Book')),
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
            name='BookListedAsRent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_received', models.DateTimeField(auto_now_add=True, verbose_name=b'Time renting began')),
                ('additional_information', models.TextField(verbose_name=b'Additional Information about book rental i.e length of rent')),
                ('return_date', models.DateTimeField(verbose_name=b'Time renting ended or should end')),
                ('type_of_rent', models.CharField(default=b'None', max_length=250, verbose_name=b"Length of Book's Rent(short, long)")),
                ('book', models.ForeignKey(to='textdoor_app.Book')),
            ],
        ),
        migrations.CreateModel(
            name='BooksYourAreRenting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('has_book_been_returned', models.BooleanField(default=False, verbose_name=b'Has book been Returned to owner?')),
                ('book', models.ForeignKey(related_name='your_book', to='textdoor_app.BookListedAsRent')),
            ],
        ),
        migrations.CreateModel(
            name='EludeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('college_attending', models.CharField(max_length=254)),
                ('new_user', models.BooleanField(default=True)),
            ],
        ),
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
        migrations.CreateModel(
            name='ListedBookForSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('additional_information', models.TextField(default=b'No additional information', verbose_name=b'Additional Information about book sold')),
                ('book', models.ForeignKey(to='textdoor_app.Book')),
                ('user', models.ForeignKey(to='textdoor_app.EludeUser')),
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
                ('date', models.DateTimeField(auto_now_add=True)),
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
            name='PurchasedBooks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('additional_information', models.TextField(verbose_name=b'Additional Information about book rental i.e length of rent')),
                ('time_book_was_bought', models.DateTimeField(verbose_name=b'Time book was bought')),
                ('book', models.ForeignKey(to='textdoor_app.Book')),
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
            name='SoldBooks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_book_was_sold', models.DateTimeField(verbose_name=b'Time book was sold')),
                ('book', models.ForeignKey(to='textdoor_app.ListedBookForSale')),
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
            model_name='eludeuser',
            name='address',
            field=models.ManyToManyField(to='textdoor_app.EludeUserAddress'),
        ),
        migrations.AddField(
            model_name='eludeuser',
            name='username',
            field=models.OneToOneField(default=b'', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='booksyourarerenting',
            name='user',
            field=models.ForeignKey(to='textdoor_app.EludeUser'),
        ),
        migrations.AddField(
            model_name='booklistedasrent',
            name='user',
            field=models.ForeignKey(to='textdoor_app.EludeUser'),
        ),
        migrations.AddField(
            model_name='bookacquiredbyrent',
            name='user',
            field=models.ForeignKey(to='textdoor_app.EludeUser'),
        ),
        migrations.AddField(
            model_name='book',
            name='book_owner',
            field=models.ForeignKey(default=b'', to='textdoor_app.EludeUser'),
        ),
    ]
