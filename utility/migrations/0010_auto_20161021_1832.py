# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-21 18:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0009_auto_20161021_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='order',
        ),
        migrations.RemoveField(
            model_name='food',
            name='owner',
        ),
        migrations.AddField(
            model_name='order',
            name='food',
            field=models.ManyToManyField(to='utility.Food'),
        ),
    ]