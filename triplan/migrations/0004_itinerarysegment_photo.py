# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-13 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triplan', '0003_itinerary_preview_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='itinerarysegment',
            name='photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
