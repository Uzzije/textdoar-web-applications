# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0002_auto_20160112_0153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eludeuser',
            name='payment_card_info',
            field=models.ManyToManyField(to='textdoor_app.PaymentCardData', blank=True),
        ),
    ]
