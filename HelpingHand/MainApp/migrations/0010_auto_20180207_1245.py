# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-07 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0009_auto_20180207_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='name',
            field=models.CharField(choices=[('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')], default='Monday', max_length=20),
        ),
    ]
