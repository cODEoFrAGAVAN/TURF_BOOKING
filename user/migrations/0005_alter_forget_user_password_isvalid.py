# Generated by Django 5.1.1 on 2024-09-17 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0004_forget_user_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="forget_user_password",
            name="isvalid",
            field=models.CharField(default="True", max_length=10),
        ),
    ]
