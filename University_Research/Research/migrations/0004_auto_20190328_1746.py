# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-28 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0003_message_latest'),
    ]

    operations = [
        migrations.AddField(
            model_name='others',
            name='time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='others',
            name='date',
            field=models.DateField(null=True),
        ),
    ]