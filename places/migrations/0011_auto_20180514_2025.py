# Generated by Django 2.0.5 on 2018-05-14 20:25

from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0010_auto_20180514_2012'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=64)),
                ('address_2', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=64)),
                ('state', localflavor.us.models.USStateField(default='PA', max_length=2)),
                ('zipcode', localflavor.us.models.USZipCodeField(max_length=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='place',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Place'),
        ),
    ]
