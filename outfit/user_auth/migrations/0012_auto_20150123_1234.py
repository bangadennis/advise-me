# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0011_userdetails_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='profile_picture',
            field=imagekit.models.fields.ProcessedImageField(default=b'images/profileImages/take_care_of_my_heart.jpg', upload_to=b'images/profileImages', blank=True),
            preserve_default=True,
        ),
    ]
