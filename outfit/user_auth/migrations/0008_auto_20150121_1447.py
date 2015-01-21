# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0007_auto_20150121_1018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clothdescription',
            old_name='user',
            new_name='user_cloth',
        ),
        migrations.AlterField(
            model_name='clothdescription',
            name='cloth_image',
            field=imagekit.models.fields.ProcessedImageField(upload_to=b'/images/wadrobe'),
        ),
    ]
