# Generated by Django 5.1.1 on 2024-09-18 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfs', '0002_turf_registration_turf_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turf_registration',
            name='turf_id',
            field=models.CharField(default='0', max_length=20, unique=True),
        ),
    ]
