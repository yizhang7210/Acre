# Generated by Django 2.0 on 2018-04-15 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('euler', '0007_move_instrument_model_to_core'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictor',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]