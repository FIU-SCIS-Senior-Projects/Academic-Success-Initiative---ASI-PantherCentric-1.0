# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 18:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0014_auto_20160710_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambassadorsurvey',
            name='session_date',
            field=models.DateField(default=datetime.datetime(2016, 7, 10, 18, 3, 28, 217541, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ambassadorsurvey',
            name='submitted_on',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 7, 10, 18, 3, 52, 643201, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tuteesurvey',
            name='session_date',
            field=models.DateField(default=datetime.datetime(2016, 7, 10, 18, 3, 58, 851566, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tuteesurvey',
            name='submitted_on',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 7, 10, 18, 4, 10, 340136, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
