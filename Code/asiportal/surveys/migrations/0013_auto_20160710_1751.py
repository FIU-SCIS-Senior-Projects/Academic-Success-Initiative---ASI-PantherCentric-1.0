# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-10 17:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.crypto
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0012_ambassadorsurvey_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ambassadorsurvey',
            name='rating_1',
        ),
        migrations.RemoveField(
            model_name='ambassadorsurvey',
            name='rating_2',
        ),
        migrations.RemoveField(
            model_name='ambassadorsurvey',
            name='rating_3',
        ),
        migrations.RemoveField(
            model_name='tuteesurvey',
            name='rating_1',
        ),
        migrations.RemoveField(
            model_name='tuteesurvey',
            name='rating_2',
        ),
        migrations.RemoveField(
            model_name='tuteesurvey',
            name='rating_3',
        ),
        migrations.AddField(
            model_name='ambassadorsurvey',
            name='canceled_session_reason',
            field=models.CharField(blank=True, max_length=140),
        ),
        migrations.AddField(
            model_name='ambassadorsurvey',
            name='session_canceled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ambassadorsurvey',
            name='survey_slug',
            field=models.SlugField(default=django.utils.crypto.get_random_string, max_length=32, unique=True),
        ),
        migrations.AddField(
            model_name='ambassadorsurvey',
            name='tutee_absent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tuteesurvey',
            name='survey_slug',
            field=models.SlugField(default=django.utils.crypto.get_random_string, max_length=32, unique=True),
        ),
        migrations.AddField(
            model_name='tuteesurvey',
            name='tutee_comments',
            field=models.CharField(default=datetime.datetime(2016, 7, 10, 17, 51, 20, 244290, tzinfo=utc), max_length=140),
            preserve_default=False,
        ),
    ]
