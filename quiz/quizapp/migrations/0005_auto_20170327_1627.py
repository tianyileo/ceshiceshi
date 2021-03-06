# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-27 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0004_auto_20170327_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfenshu',
            name='right_question',
            field=models.ManyToManyField(default=[], related_name='right_question', to='quizapp.Question'),
        ),
        migrations.AlterField(
            model_name='userfenshu',
            name='wrong_question',
            field=models.ManyToManyField(related_name='wrong_question', to='quizapp.Question'),
        ),
    ]
