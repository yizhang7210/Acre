# Generated by Django 2.0 on 2018-04-15 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('euler', '0006_make_model_parameters_static_on_predictor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='instrument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Instrument'),
        ),
        migrations.AlterField(
            model_name='trainingsample',
            name='instrument',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Instrument'),
        ),
    ]
