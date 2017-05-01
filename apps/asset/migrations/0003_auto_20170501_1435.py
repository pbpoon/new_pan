# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-01 14:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_auto_20170414_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landnum',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='area_num', to='asset.Area', verbose_name='所属区域'),
        ),
        migrations.AlterField(
            model_name='landnum',
            name='owner',
            field=models.ManyToManyField(related_name='land_num', to='asset.LandOwner', verbose_name='所有人'),
        ),
    ]