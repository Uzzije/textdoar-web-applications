# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0003_book_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookimage',
            name='book_image',
            field=models.FileField(upload_to=None, verbose_name=b'book image'),
        ),
    ]
