# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-29 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0002_auto_20190127_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='recommend',
            field=models.SmallIntegerField(choices=[(1, '☆'), (2, '☆☆'), (3, '☆☆☆'), (4, '☆☆☆☆'), (5, '☆☆☆☆☆')], default=3, verbose_name='推荐指数'),
        ),
    ]
