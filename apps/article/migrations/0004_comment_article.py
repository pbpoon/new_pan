# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-02 21:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='article.Article', verbose_name='文章'),
            preserve_default=False,
        ),
    ]
