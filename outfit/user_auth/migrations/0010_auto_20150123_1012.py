# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_auth', '0009_auto_20150121_1621'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('activity_id', models.AutoField(serialize=False, primary_key=True)),
                ('category', models.CharField(max_length=40)),
                ('event_location', models.CharField(max_length=50)),
                ('event_name', models.CharField(max_length=30)),
                ('event_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='clothdescription',
            name='cloth_image',
            field=imagekit.models.fields.ProcessedImageField(upload_to=b'images/wadrobe'),
            preserve_default=True,
        ),
    ]
