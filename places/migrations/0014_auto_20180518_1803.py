# Generated by Django 2.0.5 on 2018-05-18 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0013_auto_20180518_1417'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceChain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='place',
            name='chain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='places.PlaceChain'),
        ),
    ]
