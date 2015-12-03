# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0004_bookimage_cropping'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookacquiredbyrent',
            name='additional_information',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='bookacquiredbyrent',
            name='has_book_been_returned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bookacquiredbyrent',
            name='rented_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='bookacquiredbyrent',
            name='return_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='bookacquiredbyrent',
            name='type_of_rent',
            field=models.CharField(default=None, max_length=250),
        ),
        migrations.AlterField(
            model_name='booklistedasrent',
            name='additional_information',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='booklistedasrent',
            name='return_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='booklistedasrent',
            name='time_received',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='booklistedasrent',
            name='type_of_rent',
            field=models.CharField(default=b'None', max_length=250),
        ),
        migrations.AlterField(
            model_name='booksyourarerenting',
            name='has_book_been_returned',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='listedbookforsale',
            name='additional_information',
            field=models.TextField(default=b'No additional information'),
        ),
        migrations.AlterField(
            model_name='purchasedbooks',
            name='additional_information',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='purchasedbooks',
            name='time_book_was_bought',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='soldbooks',
            name='time_book_was_sold',
            field=models.DateTimeField(),
        ),
    ]
