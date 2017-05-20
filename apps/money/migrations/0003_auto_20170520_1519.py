# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-20 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0002_auto_20170520_1447'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='Tag',
        ),
        migrations.AlterModelOptions(
            name='moneyaccount',
            options={'ordering': ['num'], 'verbose_name': '流水账', 'verbose_name_plural': '流水账'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '标签名称', 'verbose_name_plural': '标签名称'},
        ),
        migrations.AddField(
            model_name='moneyaccount',
            name='num',
            field=models.IntegerField(default=0, verbose_name='序号'),
        ),
        migrations.AddField(
            model_name='moneyaccount',
            name='tag',
            field=models.ManyToManyField(blank=True, null=True, to='money.Tag', verbose_name='标签'),
        ),
    ]