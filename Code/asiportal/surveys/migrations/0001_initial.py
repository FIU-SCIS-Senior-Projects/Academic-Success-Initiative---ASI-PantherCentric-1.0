# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 23:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tutoring_sessions', '0005_session_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmbassadorSurvey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ambassador_surveys', to='tutoring_sessions.Session')),
            ],
        ),
    ]
