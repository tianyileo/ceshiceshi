# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 09:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0009_auto_20170327_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='zhangjie',
            name='slug',
            field=models.SlugField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='zhangjie',
            name='zhangjie_title',
            field=models.CharField(max_length=100),
        ),
    ]
