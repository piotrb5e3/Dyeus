# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 19:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0003_sensor_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sensor',
            name='is_active',
        ),
    ]
