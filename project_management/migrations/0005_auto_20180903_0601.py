# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-03 06:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_management', '0004_auto_20180827_0605'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='platform',
            field=models.CharField(blank=True, db_index=True, max_length=200, null=True),
        ),
    ]
