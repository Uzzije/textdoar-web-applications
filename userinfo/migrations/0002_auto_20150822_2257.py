# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eludeuser',
            name='user_books',
        ),
        migrations.AddField(
            model_name='book',
            name='book_owner',
            field=models.ForeignKey(default=b'', to='userinfo.EludeUser'),
        ),
    ]
