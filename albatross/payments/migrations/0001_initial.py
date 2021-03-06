# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-28 17:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('drfstripe', '0001_initial'),
        ('teams', '0005_auto_20170908_2030'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentSubscription',
            fields=[
                ('currentsubscription_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='drfstripe.CurrentSubscription')),
                ('team', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_subscription', to='teams.Team')),
            ],
            bases=('drfstripe.currentsubscription',),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='drfstripe.Customer')),
            ],
            options={
                'abstract': False,
            },
            bases=('drfstripe.customer',),
        ),
    ]
