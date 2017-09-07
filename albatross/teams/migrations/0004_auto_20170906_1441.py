# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-06 14:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_auto_20170905_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='invitation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='invitations.Invitation', verbose_name='invitation'),
        ),
    ]
