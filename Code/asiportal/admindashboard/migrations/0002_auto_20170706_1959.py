# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-06 19:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admindashboard', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='author',
        ),
        migrations.AlterField(
            model_name='note',
            name='tutee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL),
        ),
    ]
