# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 23:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0018_auto_20160719_2341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ambassadorsurvey',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='tuteesurvey',
            name='submitted',
        ),
        migrations.AddField(
            model_name='ambassadorsurvey',
            name='session_date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2016, 7, 19, 23, 43, 26, 862541, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tuteesurvey',
            name='session_date',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2016, 7, 19, 23, 43, 31, 270570, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
