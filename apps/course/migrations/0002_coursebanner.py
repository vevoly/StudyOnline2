# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-27 15:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseBanner',
            fields=[
            ],
            options={
                'verbose_name': '轮播课程',
                'verbose_name_plural': '轮播课程',
                'proxy': True,
            },
            bases=('course.course',),
        ),
    ]