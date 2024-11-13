# Generated by Django 5.1.1 on 2024-10-23 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User_reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turf_ids', models.CharField(max_length=30)),
                ('user_name', models.CharField(max_length=20, unique=True)),
                ('review_message', models.CharField(max_length=1000, null=True)),
                ('review_starts', models.CharField(default='1', max_length=1)),
            ],
        ),
    ]