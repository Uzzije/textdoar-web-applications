# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0004_auto_20150918_0406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookimage',
            name='book_image',
            field=models.ImageField(upload_to=None, verbose_name=b'book image'),
        ),
    ]
