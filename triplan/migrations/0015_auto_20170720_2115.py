# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 21:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triplan', '0014_auto_20170719_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='itinerary',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.date(2017, 7, 20)),
        ),
        migrations.AlterField(
            model_name='itinerarysegment',
            name='category',
            field=models.IntegerField(choices=[(0, 'Food'), (1, 'Educational'), (2, 'Outdoor'), (3, 'Games'), (4, 'Social'), (5, 'Shopping'), (6, 'Casino'), (7, 'Recreational'), (8, 'Photo-spot'), (9, 'Transport'), (10, 'Flight'), (11, 'Other')], default=0),
        ),
    ]
