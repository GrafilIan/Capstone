# Generated by Django 4.2.4 on 2023-10-03 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0054_timerecord_interns_calendar_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timerecord',
            name='timestamp',
            field=models.DateTimeField(default=None),
        ),
    ]
