# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccountData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_on_bank_account', models.CharField(max_length=1000)),
                ('bank_token_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='eludeuser',
            name='phone_number',
            field=models.CharField(default=b'000-000-0000', max_length=15),
        ),
        migrations.AddField(
            model_name='eludeuseraddress',
            name='current_shipping_address',
            field=models.BooleanField(default=True),
        ),
    ]
