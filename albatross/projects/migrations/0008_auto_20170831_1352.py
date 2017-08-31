# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 13:52
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth import get_user_model

def populate_team(apps, schema_editor):
    Team = apps.get_model('teams', 'Team')
    Project = apps.get_model('projects', 'Project')
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(id=1)
    except UserModel.DoesNotExist:
        user = UserModel.objects.create(
            email='test@test.com',
            first_name='Tester',
            last_name='Account',
            password='password125',
            username='test@test.com'
        )
    team = Team.objects.create(name='Krit', creator_id=1)
    for project in Project.objects.all():
        project.team = team

class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_project_team'),
    ]

    operations = [
        migrations.RunPython(populate_team),
    ]
