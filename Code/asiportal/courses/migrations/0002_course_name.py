# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 21:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='name',
            field=models.CharField(default='Dicky', max_length=10),
            preserve_default=False,
        ),
    ]
