# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-23 17:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0006_document'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='moneyaccount',
            options={'ordering': ['type', 'num'], 'verbose_name': '流水账', 'verbose_name_plural': '流水账'},
        ),
        migrations.AddField(
            model_name='document',
            name='thumb',
            field=models.ImageField(blank=True, upload_to='upload/thumb'),
        ),
        migrations.AlterField(
            model_name='document',
            name='img',
            field=models.ImageField(max_length=120, upload_to='file/money/%Y%m%d', verbose_name='留档图片'),
        ),
        migrations.AlterField(
            model_name='document',
            name='money_num',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc', to='money.MoneyAccount', verbose_name='对应账款'),
        ),
    ]
