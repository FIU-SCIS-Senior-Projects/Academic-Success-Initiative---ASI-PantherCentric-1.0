# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-31 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0028_auto_20160825_0204'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuteesurvey',
            name='wearing_shirt',
            field=models.BooleanField(default=False),
        ),
    ]
