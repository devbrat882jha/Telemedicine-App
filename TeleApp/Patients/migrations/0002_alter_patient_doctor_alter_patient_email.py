# Generated by Django 5.0.3 on 2024-03-16 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctors', '0001_initial'),
        ('Patients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='doctor',
            field=models.ManyToManyField(blank=True, null=True, related_name='doctors', to='Doctors.doctor'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
