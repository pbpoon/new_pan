# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-01 23:32
from __future__ import unicode_literals

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20170531_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='mardownx',
            field=markdownx.models.MarkdownxField(default=1),
            preserve_default=False,
        ),
    ]