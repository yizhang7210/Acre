# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-22 03:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euler', '0004_add_predictions_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='prediction',
            name='score',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]