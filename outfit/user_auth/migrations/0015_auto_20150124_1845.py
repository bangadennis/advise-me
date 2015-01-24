# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0014_clothfactbase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clothdescription',
            name='cloth_description',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='category',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='useractivity',
            name='event_name',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='occupation',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='skintone',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
