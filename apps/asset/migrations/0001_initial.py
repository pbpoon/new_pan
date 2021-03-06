# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-27 23:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='区域名称')),
                ('desc', models.CharField(blank=True, max_length=60, null=True, verbose_name='分类描述')),
            ],
            options={
                'verbose_name': '区域名称',
                'verbose_name_plural': '区域名称',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='分类名称')),
                ('desc', models.CharField(blank=True, max_length=60, null=True, verbose_name='分类描述')),
            ],
            options={
                'verbose_name': '分类名称',
                'verbose_name_plural': '分类名称',
            },
        ),
        migrations.CreateModel(
            name='LandNum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.CharField(db_index=True, max_length=10, verbose_name='田地号码')),
                ('fm', models.DecimalField(decimal_places=2, help_text='单位为分岁', max_digits=5, verbose_name='分亩')),
                ('is_rent', models.BooleanField(default=False, verbose_name='是否出租')),
                ('ps', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注信息')),
                ('desc', models.CharField(blank=True, max_length=60, null=True, verbose_name='分类描述')),
                ('is_del', models.BooleanField(default=False, verbose_name='注销')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='area_num', to='asset.Area', verbose_name='所属区域')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='land_num', to='asset.Category', verbose_name='分类名称')),
            ],
            options={
                'verbose_name': '田地信息',
                'verbose_name_plural': '田地信息',
            },
        ),
        migrations.CreateModel(
            name='LandOwner',
            fields=[
            ],
            options={
                'verbose_name': '田地所属于人信息',
                'verbose_name_plural': '田地所属于人信息',
                'proxy': True,
            },
            bases=('account.people',),
        ),
        migrations.AddField(
            model_name='landnum',
            name='owner',
            field=models.ManyToManyField(related_name='land_num', to='asset.LandOwner', verbose_name='所有人'),
        ),
    ]
