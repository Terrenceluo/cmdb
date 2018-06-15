# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-15 22:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20180614_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='software',
            name='asset',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='assets.Asset'),
            preserve_default=False,
        ),
    ]