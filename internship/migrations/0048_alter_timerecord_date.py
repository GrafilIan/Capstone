# Generated by Django 4.2.4 on 2023-10-03 03:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0047_timerecord_date_alter_timerecord_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timerecord',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]