# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-01 08:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20171201_0830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
