# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0006_auto_20150120_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='profile_picture',
            field=imagekit.models.fields.ProcessedImageField(upload_to=b'images/profileImages', blank=True),
        ),
    ]
