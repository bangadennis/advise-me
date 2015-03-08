# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_auto_20150223_1906'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clothfactbase',
            old_name='cloth_id',
            new_name='cloth',
        ),
    ]
