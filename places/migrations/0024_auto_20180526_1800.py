# Generated by Django 2.0.5 on 2018-05-26 18:00

import autoslug.fields
from django.conf import settings
from django.db import migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0023_auto_20180524_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=True, populate_from='title'),
        ),
    ]
