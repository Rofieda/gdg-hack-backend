# Generated by Django 5.0.2 on 2025-02-08 03:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_hackathon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskexchange',
            name='student2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_exchanges_received', to='account.studentprofile'),
        ),
    ]
