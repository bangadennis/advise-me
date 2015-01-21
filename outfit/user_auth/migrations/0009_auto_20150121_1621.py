# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0008_auto_20150121_1447'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clothdescription',
            old_name='user_cloth',
            new_name='user',
        ),
    ]
