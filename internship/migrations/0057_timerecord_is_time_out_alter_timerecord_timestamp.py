# Generated by Django 4.2.4 on 2023-10-03 07:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0056_alter_timerecord_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='timerecord',
            name='is_time_out',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='timerecord',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 3, 15, 2, 36, 316796)),
        ),
    ]