# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-27 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0003_auto_20180823_0551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]