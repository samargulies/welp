# Generated by Django 2.0.5 on 2018-05-14 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0011_auto_20180514_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='current',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='address',
            name='sort_value',
            field=models.SmallIntegerField(default=0),
        ),
    ]
