# Generated by Django 5.1.1 on 2024-10-17 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("turfs", "0009_turf_bank_details"),
    ]

    operations = [
        migrations.AlterField(
            model_name="turf_bank_details",
            name="bank_account_number",
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name="turf_bank_details",
            name="turf_id",
            field=models.CharField(max_length=50, unique=True),
        ),
    ]