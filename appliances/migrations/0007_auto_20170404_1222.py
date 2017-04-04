# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 12:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appliances', '0006_auto_20170313_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliance',
            name='authentication_model',
            field=models.CharField(choices=[('token', 'Token'), ('gcm_aes', 'GCM + AES128'), ('sha_mac', 'SHA256 HMAC')], max_length=16),
        ),
    ]
