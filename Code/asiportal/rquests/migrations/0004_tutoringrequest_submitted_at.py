# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-18 03:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rquests', '0003_tutoringrequest_availability'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutoringrequest',
            name='submitted_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 6, 18, 3, 20, 40, 33053, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
