# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 13:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='toggl_api_key',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]