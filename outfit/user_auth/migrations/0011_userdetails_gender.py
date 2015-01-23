# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0010_auto_20150123_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='gender',
            field=models.CharField(default=b'Male', max_length=10),
            preserve_default=True,
        ),
    ]
