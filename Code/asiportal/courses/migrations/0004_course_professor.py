# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='professor',
            field=models.CharField(default='Idris Mercer', max_length=25),
            preserve_default=False,
        ),
    ]
