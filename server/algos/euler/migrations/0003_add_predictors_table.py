# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-14 10:48
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euler', '0002_change_number_fields_to_decimals'),
    ]

    operations = [
        migrations.CreateModel(
            name='Predictor',
            fields=[
                ('name', models.CharField(max_length=40, primary_key=True, serialize=False, unique=True)),
                ('parameter_range', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
    ]
