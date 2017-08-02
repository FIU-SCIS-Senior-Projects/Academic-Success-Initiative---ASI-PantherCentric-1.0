# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 20:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('tutoring_sessions', '0004_auto_20160617_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='course_sessions', to='courses.Course'),
            preserve_default=False,
        ),
    ]
