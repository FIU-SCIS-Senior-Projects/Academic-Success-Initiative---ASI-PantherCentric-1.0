# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 15:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('availabilities', '0005_auto_20160706_1049'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='availability',
            unique_together=set([]),
        ),
    ]
