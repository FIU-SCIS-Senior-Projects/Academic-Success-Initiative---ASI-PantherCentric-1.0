# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-01 00:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0006_auto_20160629_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ambassadorsurvey',
            name='session',
        ),
        migrations.RemoveField(
            model_name='tuteesurvey',
            name='session',
        ),
        migrations.DeleteModel(
            name='AmbassadorSurvey',
        ),
        migrations.DeleteModel(
            name='TuteeSurvey',
        ),
    ]
