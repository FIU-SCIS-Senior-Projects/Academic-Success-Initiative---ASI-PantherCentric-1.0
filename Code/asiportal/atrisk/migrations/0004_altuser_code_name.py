# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-25 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atrisk', '0003_auto_20170124_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='altuser',
            name='code_name',
            field=models.CharField(default='doogie', max_length=20),
            preserve_default=False,
        ),
    ]
