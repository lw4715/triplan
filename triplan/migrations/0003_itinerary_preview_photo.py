# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-13 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triplan', '0002_auto_20170712_2226'),
    ]

    operations = [
        migrations.AddField(
            model_name='itinerary',
            name='preview_photo',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
