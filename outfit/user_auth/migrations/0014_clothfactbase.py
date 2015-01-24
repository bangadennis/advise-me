# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0013_auto_20150123_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClothFactBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cloth_type', models.CharField(max_length=50)),
                ('cloth_color', models.CharField(max_length=50)),
                ('cloth_material', models.CharField(max_length=50)),
                ('cloth_print', models.CharField(max_length=50)),
                ('cloth_id', models.ForeignKey(to='user_auth.ClothDescription')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
