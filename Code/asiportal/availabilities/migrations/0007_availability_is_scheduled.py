# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-20 21:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('availabilities', '0006_auto_20160707_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='availability',
            name='is_scheduled',
            field=models.BooleanField(default=False),
        ),
    ]
