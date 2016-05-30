# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import image_cropping.fields
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
                ('book_condition', models.CharField(max_length=25)),
                ('author', models.CharField(max_length=500)),
                ('sales_price', models.CharField(default=b'0.00', max_length=500)),
                ('publish_date', models.DateTimeField(default=datetime.datetime.now, db_index=True, blank=True)),
                ('publish_type', models.CharField(default=b'Now', max_length=15)),
                ('slug', models.SlugField(max_length=100)),
                ('book_edition', models.CharField(max_length=100, blank=True)),
                ('book_description', models.CharField(default=b'', max_length=6000, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image_name', models.CharField(max_length=100)),
                ('book_image', models.ImageField(upload_to=b'image/%Y/%m/%d', verbose_name=b'book image')),
                (b'cropping', image_cropping.fields.ImageRatioField(b'book_image', '60x60', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cropping')),
                ('book', models.ForeignKey(default=b'', to='textdoor_app.Book')),
            ],
        ),
        migrations.CreateModel(
            name='EludeUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('college_attending', models.CharField(max_length=254)),
                ('new_user', models.BooleanField(default=True)),
                ('stripe_account_activated', models.BooleanField(default=False)),
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
            name='PaymentCardData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_id', models.CharField(default=b'No customer ID', max_length=1000)),
                ('is_user_current_option', models.BooleanField(default=False)),
                ('address', models.CharField(default=b'No Address', max_length=1000)),
                ('address_state', models.CharField(default=b'No State', max_length=100)),
                ('address_country', models.CharField(default=b'No Country', max_length=100)),
                ('address_zip_code', models.CharField(default=b'No Zip Code', max_length=100)),
                ('exp_month', models.CharField(default=b'No exp month', max_length=10)),
                ('exp_year', models.CharField(default=b'No exp year', max_length=10)),
                ('last_4_of_card', models.CharField(default=b'No last Four', max_length=10)),
                ('card_brand', models.CharField(default=b'No card brand', max_length=100)),
                ('funding_type', models.CharField(default=b'No funding type', max_length=100)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedBooks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('additional_information', models.TextField()),
                ('time_book_was_bought', models.DateTimeField()),
                ('book', models.ForeignKey(to='textdoor_app.Book')),
                ('user', models.ForeignKey(to='textdoor_app.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='RepGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'Applied', max_length=100)),
                ('user', models.ForeignKey(to='textdoor_app.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='SoldBooks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_book_was_sold', models.DateTimeField()),
                ('book', models.ForeignKey(to='textdoor_app.Book')),
                ('user', models.ForeignKey(to='textdoor_app.EludeUser')),
            ],
        ),
        migrations.CreateModel(
            name='StripeData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token_type', models.CharField(default=None, max_length=1000)),
                ('stripe_publishable_key', models.CharField(default=None, max_length=1000)),
                ('scope', models.CharField(default=None, max_length=1000)),
                ('stripe_user_id', models.CharField(default=None, max_length=1000)),
                ('refresh_token', models.CharField(default=None, max_length=1000)),
                ('access_token', models.CharField(default=None, max_length=1000)),
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
            name='payment_card_info',
            field=models.ManyToManyField(to='textdoor_app.PaymentCardData'),
        ),
        migrations.AddField(
            model_name='eludeuser',
            name='stripe_data',
            field=models.ForeignKey(blank=True, to='textdoor_app.StripeData', null=True),
        ),
        migrations.AddField(
            model_name='eludeuser',
            name='username',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='book_owner',
            field=models.ForeignKey(default=b'', to='textdoor_app.EludeUser'),
        ),
    ]
