# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 17:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invitations', '0002_auto_20170831_1331'),
        ('teams', '0002_auto_20170831_1331'),
    ]

    operations = [
        migrations.RenameField('membership', 'invite', 'invitation'),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('team', 'user', 'invitation')]),
        ),
    ]