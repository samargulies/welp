# Generated by Django 2.0.5 on 2018-05-19 16:43

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0016_auto_20180519_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
