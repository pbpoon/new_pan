# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-27 11:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('money', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='moneyaccount',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='经手人'),
        ),
        migrations.AddField(
            model_name='moneyaccount',
            name='tag',
            field=models.ManyToManyField(null=True, to='money.Tag', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='document',
            name='money_num',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc', to='money.MoneyAccount', verbose_name='对应账款'),
        ),
    ]
