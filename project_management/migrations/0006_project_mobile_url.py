# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-04 06:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0005_auto_20180903_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='mobile_url',
            field=models.URLField(blank=True, null=True, verbose_name=b'Mobile URL'),
        ),
    ]