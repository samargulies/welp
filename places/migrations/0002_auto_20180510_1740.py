# Generated by Django 2.0.5 on 2018-05-10 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='user_images/%Y/%m/%d')),
                ('title', models.CharField(blank=True, max_length=256)),
                ('description', models.TextField(blank=True)),
                ('alt', models.CharField(blank=True, max_length=256)),
                ('attribution', models.CharField(blank=True, max_length=256)),
                ('license', models.CharField(blank=True, max_length=256)),
            ],
        ),
        migrations.AlterField(
            model_name='place',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='place',
            name='images',
            field=models.ManyToManyField(to='places.Image'),
        ),
    ]
