# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_auto_20171019_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
