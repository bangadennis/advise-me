# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0012_auto_20150123_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothdescription',
            name='cloth_description',
            field=models.CharField(max_length=30),
            preserve_default=True,
        ),
    ]
