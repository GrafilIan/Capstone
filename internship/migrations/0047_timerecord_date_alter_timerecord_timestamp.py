# Generated by Django 4.2.4 on 2023-10-03 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0046_timerecord_interns_calendar'),
    ]

    operations = [
        migrations.AddField(
            model_name='timerecord',
            name='date',
            field=models.DateField(default=None),  # Specify a valid default value
        ),
        migrations.AlterField(
            model_name='timerecord',
            name='timestamp',
            field=models.DateTimeField(default=None),  # Specify a valid default value
        ),
    ]
