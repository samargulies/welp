# Generated by Django 2.0.5 on 2018-05-20 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0016_auto_20180519_1624'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='license',
        ),
    ]
