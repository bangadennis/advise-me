# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_auto_20150119_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='occupation',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='skincolor',
            field=models.CharField(max_length=30),
        ),
    ]
