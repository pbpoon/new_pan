# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-20 14:46
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='分类名称')),
                ('desc', models.CharField(blank=True, max_length=60, null=True, verbose_name='分类描述')),
                ('create_d', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '分类名称',
                'verbose_name_plural': '分类名称',
            },
        ),
        migrations.CreateModel(
            name='MoneyAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date(2017, 5, 20), verbose_name='日期')),
                ('detail', models.CharField(max_length=120, verbose_name='项目')),
                ('status', models.CharField(choices=[('-1', '支出'), ('1', '收入')], max_length=2, verbose_name='去向')),
                ('type', models.CharField(choices=[('b', '银行'), ('c', '现金')], max_length=1, verbose_name='账目类型')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='金额')),
                ('ps', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注说明')),
                ('create_d', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_d', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='经手人')),
            ],
            options={
                'verbose_name': '银行流水账',
                'verbose_name_plural': '银行流水账',
                'ordering': ['-date'],
            },
        ),
    ]
