# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-27 23:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=12, unique=True, verbose_name='户名号码')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
            ],
            options={
                'verbose_name': '户口号码',
                'verbose_name_plural': '户口号码',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='People',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=8, verbose_name='姓氏')),
                ('last_name', models.CharField(max_length=12, verbose_name='名字')),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女')], max_length=6, verbose_name='性别')),
                ('id_card_num', models.CharField(blank=True, db_index=True, max_length=18, null=True, verbose_name='身份证号码')),
                ('is_main', models.BooleanField(default=False, verbose_name='是否为户主')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='出生日期')),
                ('is_marry', models.BooleanField(default=False, verbose_name='是否已婚')),
                ('is_getmoney', models.BooleanField(default=False, verbose_name='分钱资格')),
                ('join_d', models.DateField(blank=True, null=True, verbose_name='入户日期')),
                ('nationality', models.CharField(blank=True, max_length=26, null=True, verbose_name='民族')),
                ('education', models.CharField(blank=True, max_length=20, null=True, verbose_name='教育程度')),
                ('account_type', models.CharField(blank=True, max_length=20, null=True, verbose_name='户口类型')),
                ('phone_num', models.CharField(blank=True, max_length=11, null=True, verbose_name='电话号码')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否注销')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='people', to='account.Account', verbose_name='所属户口')),
            ],
            options={
                'verbose_name': '村民信息',
                'verbose_name_plural': '村民信息',
            },
        ),
    ]
