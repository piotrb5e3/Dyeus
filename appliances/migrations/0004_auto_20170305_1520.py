# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-05 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appliances', '0003_auto_20170305_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliance',
            name='authentication_value',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
