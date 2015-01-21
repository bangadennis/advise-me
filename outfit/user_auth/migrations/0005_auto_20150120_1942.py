# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0004_auto_20150120_1940'),
    ]

    operations = [
        migrations.RenameField(
            model_name='useractivity',
            old_name='user_id',
            new_name='user_id1',
        ),
    ]
