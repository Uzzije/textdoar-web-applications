# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import image_cropping.fields


class Migration(migrations.Migration):

    dependencies = [
        ('textdoor_app', '0003_remove_listedbookforsale_make_it_availiable'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookimage',
            name=b'cropping',
            field=image_cropping.fields.ImageRatioField(b'image', '430x360', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='cropping'),
        ),
    ]
