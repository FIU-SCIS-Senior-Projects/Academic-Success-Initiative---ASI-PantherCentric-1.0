# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ambassadorsurvey',
            name='rating_1',
            field=models.IntegerField(default=1),
        ),
    ]
