# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0005_auto_20150120_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useractivity',
            name='user_id1',
        ),
        migrations.DeleteModel(
            name='UserActivity',
        ),
        migrations.RenameField(
            model_name='clothdescription',
            old_name='user_id',
            new_name='user',
        ),
    ]
