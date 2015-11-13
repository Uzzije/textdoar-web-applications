# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0005_auto_20150919_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookimage',
            name='book_image',
            field=models.ImageField(upload_to=b'media', verbose_name=b'book image'),
        ),
    ]
