# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-19 15:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20160719_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='professor',
        ),
    ]
