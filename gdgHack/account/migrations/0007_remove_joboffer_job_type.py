# Generated by Django 5.0.2 on 2025-02-08 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_virtualexperience_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joboffer',
            name='job_type',
        ),
    ]
