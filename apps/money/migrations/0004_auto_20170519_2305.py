# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 23:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0003_auto_20170519_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyaccount',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 19, 23, 5, 34, 236469), verbose_name='日期'),
        ),
    ]
