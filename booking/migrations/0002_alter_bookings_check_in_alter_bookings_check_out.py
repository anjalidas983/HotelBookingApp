# Generated by Django 4.2.3 on 2023-08-12 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='check_in',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='check_out',
            field=models.DateField(),
        ),
    ]
