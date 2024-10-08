# Generated by Django 5.1.1 on 2024-10-09 07:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Store_order_id",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("booking_id", models.CharField(max_length=20, unique=True)),
                ("payment_id", models.CharField(max_length=20)),
                ("payment_status", models.CharField(default="PENDING", max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name="booking",
            name="booking_date_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="booking",
            name="payment_status",
            field=models.CharField(default="PENDING", max_length=20),
        ),
        migrations.AlterField(
            model_name="booking",
            name="slot_end_date_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="booking",
            name="slot_start_date_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
