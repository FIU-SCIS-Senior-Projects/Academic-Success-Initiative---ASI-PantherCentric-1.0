# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-08 03:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20170308_0352'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectts',
            options={'permissions': (('approve_project_ts', 'Can approve timesheet'),)},
        ),
        migrations.AlterField(
            model_name='projectts',
            name='ambassador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_ts_member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projecttsentry',
            name='project_time_sheet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_ts', to='projects.ProjectTS'),
        ),
    ]
