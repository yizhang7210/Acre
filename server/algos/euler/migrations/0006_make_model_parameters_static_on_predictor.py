# Generated by Django 2.0 on 2018-04-15 01:44

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('euler', '0005_add_prediction_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prediction',
            name='predictor_params',
        ),
        migrations.RemoveField(
            model_name='predictor',
            name='parameter_range',
        ),
        migrations.AddField(
            model_name='predictor',
            name='parameters',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
