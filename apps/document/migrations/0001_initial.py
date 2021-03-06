# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-27 23:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import document.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=20, verbose_name='名称')),
                ('desc', models.CharField(blank=True, max_length=60, null=True, verbose_name='描述')),
                ('create_d', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_d', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('views', models.IntegerField(default=0, verbose_name='查阅量')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document', to='document.Category', verbose_name='分类名称')),
            ],
            options={
                'verbose_name': '档案名称',
                'verbose_name_plural': '档案名称',
            },
        ),
        migrations.CreateModel(
            name='DocumentItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='名称')),
                ('file', models.FileField(upload_to=document.models.get_upload_to, verbose_name='文件')),
                ('desc', models.CharField(blank=True, max_length=60, null=True, verbose_name='描述')),
                ('format', models.CharField(default='jpg', max_length=12, verbose_name='文件格式')),
                ('update_d', models.DateTimeField(auto_now=True, verbose_name='更新日期')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='document.Document', verbose_name='分类名称')),
            ],
            options={
                'verbose_name': '档案名称',
                'verbose_name_plural': '档案名称',
            },
        ),
    ]
