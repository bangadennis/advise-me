# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClothDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cloth_image', imagekit.models.fields.ProcessedImageField(upload_to=b'images/wadrobe')),
                ('cloth_description', models.CharField(max_length=50)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='UserActivity',
            fields=[
                ('activity_id', models.AutoField(serialize=False, primary_key=True)),
                ('category', models.CharField(max_length=50)),
                ('event_location', models.CharField(max_length=50)),
                ('event_name', models.CharField(max_length=50)),
                ('event_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(default=b'Male', max_length=10)),
                ('dateofbirth', models.DateField()),
                ('skintone', models.CharField(max_length=50)),
                ('occupation', models.CharField(max_length=50)),
                ('profile_picture', imagekit.models.fields.ProcessedImageField(default=b'images/profileImages/take_care_of_my_heart.jpg', upload_to=b'images/profileImages', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
