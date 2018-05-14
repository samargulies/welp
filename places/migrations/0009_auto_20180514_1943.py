# Generated by Django 2.0.5 on 2018-05-14 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0008_auto_20180514_0208'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagecategory',
            options={'verbose_name': 'Image Category', 'verbose_name_plural': 'Image Categories'},
        ),
        migrations.AlterModelOptions(
            name='placecategory',
            options={'verbose_name': 'Place Category', 'verbose_name_plural': 'Place Categories'},
        ),
        migrations.AddField(
            model_name='place',
            name='address',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='categories',
            field=models.ManyToManyField(blank=True, to='places.ImageCategory'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='place',
            name='categories',
            field=models.ManyToManyField(blank=True, to='places.PlaceCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='imagecategory',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='placecategory',
            unique_together=set(),
        ),
    ]
