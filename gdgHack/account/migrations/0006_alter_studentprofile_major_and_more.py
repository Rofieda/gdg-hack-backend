# Generated by Django 5.0.2 on 2025-02-07 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_enterpriseprofile_name_enterpriseprofile_web_site_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprofile',
            name='major',
            field=models.CharField(choices=[('CS', 'Computer Science'), ('EE', 'Electrical Engineering'), ('ME', 'Mechanical Engineering'), ('CE', 'Civil Engineering'), ('BIO', 'Biotechnology'), ('AUTRE', 'Autre')], default='AUTRE', max_length=10),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='university',
            field=models.CharField(choices=[('ENP', 'ENP'), ('USTHB', 'USTHB'), ('ESI', 'ESI'), ('UMBB', 'UMBB'), ('AUTRE', 'Autre')], default='AUTRE', max_length=10),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='year_studying',
            field=models.CharField(choices=[('1st', '1st Year'), ('2nd', '2nd Year'), ('3rd', '3rd Year'), ('4th', '4th Year'), ('AUTRE', 'Autre')], default='AUTRE', max_length=10),
        ),
    ]
