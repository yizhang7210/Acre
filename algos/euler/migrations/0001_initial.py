# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 23:24
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('datasource', '0003_add_unique_together_for_candles'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('features', django.contrib.postgres.fields.ArrayField(base_field=models.FloatField(), size=7)),
                ('target', models.FloatField()),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='datasource.Instrument')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='trainingsample',
            unique_together=set([('instrument', 'date')]),
        ),
    ]
