# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-17 18:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring_sessions', '0003_session_tutee'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2016, 6, 17, 18, 31, 8, 791928, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='session',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2016, 6, 17, 18, 31, 11, 807852, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
