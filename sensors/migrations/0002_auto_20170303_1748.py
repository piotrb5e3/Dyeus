# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-03 17:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorvalue',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sensor_values', to='sensors.Sensor'),
        ),
    ]