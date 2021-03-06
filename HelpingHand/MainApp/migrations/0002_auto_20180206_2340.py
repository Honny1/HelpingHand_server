# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-06 23:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='state',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='configuration',
            name='time',
            field=models.TimeField(default=datetime.datetime(2018, 2, 6, 23, 40, 15, 170934)),
        ),
        migrations.AlterField(
            model_name='day',
            name='name',
            field=models.CharField(choices=[('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Su    nday')], default='Monday', max_length=20),
        ),
        migrations.AlterField(
            model_name='device',
            name='state',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=30),
        ),
    ]
