# Generated by Django 3.2 on 2025-01-04 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0002_auto'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
