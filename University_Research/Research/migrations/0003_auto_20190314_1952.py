# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-14 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Research', '0002_auto_20190301_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='scholar',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='thesis',
            name='datePaid',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='thesis',
            name='fees',
            field=models.CharField(default=0, max_length=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='su_personal_det',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
