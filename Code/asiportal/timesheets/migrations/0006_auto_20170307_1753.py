# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-07 17:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timesheets', '0005_auto_20170307_0214'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tutoringtimesheetentry',
            options={'permissions': (('approve_entry', 'Can Approve Entries'),)},
        ),
    ]
